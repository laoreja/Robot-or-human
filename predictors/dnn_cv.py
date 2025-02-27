from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import sys
from sklearn.metrics import roc_auc_score
from new_commons import *

name = "DNN_CV_2"
FEATURE_DIM = 668
BASE_LEARNING_RATE = 0.0001
BATCH_SIZE = 100
#DECAY_STEP = 100000 # 14 step per epoch
#DECAY_RATE = 0.33
MAX_EPOCH = 30
do_CV = False
do_train = True
do_test = True
K = 10
LOG_DIR_base = 'dnn_cv_2_'

def _variable_with_weight_decay(name, shape, stddev, wd, use_xavier=True):
    if use_xavier:
        initializer = tf.contrib.layers.xavier_initializer()
    else:
        initializer = tf.truncated_normal_initializer(stddev=stddev)
    var = tf.get_variable(name, shape, initializer=initializer, dtype=tf.float32)
    if wd is not None:
        weight_decay = tf.multiply(tf.nn.l2_loss(var), wd, name='weight_loss')
        tf.add_to_collection('losses', weight_decay)
    return var

def fully_connected(inputs,
                    num_outputs,
                    scope,
                    use_xavier=True,
                    stddev=1e-3,
                    weight_decay=1e-4,
                    activation_fn=tf.nn.relu,
                    bn=False,
                    bn_decay=0.0,
                    is_training=None):
    with tf.variable_scope(scope) as sc:
        num_input_units = inputs.get_shape()[-1].value
        weights = _variable_with_weight_decay('weights',
                                                shape=[num_input_units, num_outputs],
                                                use_xavier=use_xavier,
                                                stddev=stddev,
                                                wd=weight_decay)
        outputs = tf.matmul(inputs, weights)
        biases = tf.get_variable('biases', [num_outputs], initializer=tf.constant_initializer(0.0), dtype=tf.float32)
        outputs = tf.nn.bias_add(outputs, biases)
        if bn:
            outputs = tf.contrib.layers.batch_norm(
                                outputs, decay=bn_decay, center=True, scale=True, is_training=is_training, fused=True, scope='bn')

        if activation_fn is not None:
            outputs = activation_fn(outputs)
        return outputs


def dropout(inputs,
            is_training,
            scope,
            keep_prob=0.5,
            noise_shape=None):
    with tf.variable_scope(scope) as sc:
        outputs = tf.cond(is_training,
                        lambda: tf.nn.dropout(inputs, keep_prob, noise_shape),
                        lambda: inputs)
        return outputs


def dnn_model(features, is_training):
    net = fully_connected(features, 256, scope='fc1', is_training=is_training)
    net = dropout(net, is_training, scope='dp1', keep_prob = 0.8)
    net = fully_connected(net, 128, scope='fc2', is_training=is_training)
    net = dropout(net, is_training, scope='dp2', keep_prob = 0.6)    
    net = fully_connected(net, 2, scope='fc_final', is_training=is_training, activation_fn=None)
    return net

def get_loss(pred, label):
#    print(label)
#    print(pred)
    loss = tf.nn.weighted_cross_entropy_with_logits(targets=tf.cast(label, tf.float32),
    logits=pred[:, 1] - pred[:, 0],
    pos_weight=19)
#    loss = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=pred, labels=label)
    classify_loss = tf.reduce_mean(loss)
    return classify_loss

def get_learning_rate(step):
#    learning_rate = tf.train.exponential_decay(
#                        BASE_LEARNING_RATE,  # Base learning rate.
#                        step * BATCH_SIZE,  # Current index into the dataset.
#                        DECAY_STEP,          # Decay step.
#                        DECAY_RATE,          # Decay rate.
#                        staircase=True)
#    learning_rate = tf.maximum(learning_rate, 0.00001) # CLIP THE LEARNING RATE!
#    return learning_rate        
    return BASE_LEARNING_RATE

    
def train(MAX_EPOCH, train_data, train_labels, eval_data, eval_labels, LOG_DIR):
    with tf.Graph().as_default():
        features_pl = tf.placeholder(tf.float32, shape=(None, FEATURE_DIM))
        labels_pl = tf.placeholder(tf.int32, shape=(None))
        is_training_pl = tf.placeholder(tf.bool, shape=())
        
        pred = dnn_model(features_pl, is_training_pl)
        loss = get_loss(pred, labels_pl)
        
        step = tf.Variable(0)
        learning_rate = get_learning_rate(step)
        
        optimizer = tf.train.AdamOptimizer(learning_rate)
        train_op = optimizer.minimize(loss, global_step=step)
        
        saver = tf.train.Saver()
        
        sess = tf.Session()
        init = tf.global_variables_initializer()
        sess.run(init, {is_training_pl: True})
        
        best_eval_auc = None
        best_eval_accuracy = None
        best_eval_epoch = None
        for epoch in range(MAX_EPOCH):            
#            # overfit small
#            batch_data = train_data[-38:, :]
#            batch_labels = train_labels[-38:]            
#            _, _, pred_val, loss_val = sess.run([step, train_op, pred, loss], feed_dict={features_pl:batch_data, labels_pl:batch_labels, is_training_pl:True})
#            pred_val = np.argmax(pred_val, 1)
#            correct = np.sum(pred_val == batch_labels)
#            print('epoch loss: %f, accuracy: %f' % (loss_val, correct / float(38)))


            # train
            p = np.random.permutation(train_data.shape[0])
            train_data = train_data[p,:]
            train_labels = train_labels[p]
            
            start_idx = 0
            total_correct = 0
            total_seen = 0
            loss_sum = 0
            num_batches = train_data.shape[0]//BATCH_SIZE
            
            probability = np.zeros(num_batches * BATCH_SIZE)
            while(True):
                end_idx = start_idx + BATCH_SIZE
                batch_data = train_data[start_idx:end_idx, :]
                batch_labels = train_labels[start_idx:end_idx]

                _, _, pred_val, loss_val = sess.run([step, train_op, pred, loss], feed_dict={features_pl:batch_data, labels_pl:batch_labels, is_training_pl:True})
                new_pred_val = np.argmax(pred_val, 1)
                correct = np.sum(new_pred_val == batch_labels)
                total_correct += correct
                total_seen += BATCH_SIZE
                loss_sum += loss_val
                
                normed_pred_val = pred_val - np.max(pred_val, axis=1)[:, None]
                probability[start_idx:end_idx] = np.exp(normed_pred_val[:, 1]) / np.sum(np.exp(normed_pred_val),axis=1)
                
                start_idx += BATCH_SIZE
                if start_idx + BATCH_SIZE > train_data.shape[0]:
                    break
#            if epoch % 10 == 9:
            train_auc = roc_auc_score(train_labels[:num_batches * BATCH_SIZE], probability)
            print('epoch: %d, loss: %f, \taccuracy: %f, \tAUC: %f' % (epoch, loss_sum / float(num_batches), total_correct / float(total_seen), train_auc))
            
            # eval
            _, pred_val, loss_val = sess.run([step, pred, loss], feed_dict={features_pl:eval_data, labels_pl:eval_labels, is_training_pl:False})
            
            new_pred_val = np.argmax(pred_val, 1)
            eval_accuracy = np.mean(new_pred_val == eval_labels)
            
            normed_pred_val = pred_val - np.max(pred_val, axis=1)[:, None]
            probability = np.exp(normed_pred_val[:, 1]) / np.sum(np.exp(normed_pred_val),axis=1)
            eval_auc = roc_auc_score(eval_labels, probability)
#            equal_auc = roc_auc_score(eval_labels[-38:], probability[-38:])

            if best_eval_auc is None or eval_auc > best_eval_auc:
                best_eval_auc = eval_auc
                best_eval_accuracy = eval_accuracy
                best_eval_epoch = epoch
                save_path = saver.save(sess, os.path.join(LOG_DIR, "model_best.ckpt"))
            
#            if epoch % 10 == 9:
            print('     eval loss: %f, \taccuracy: %f, \tAUC: %f\n' % (loss_val, eval_accuracy, eval_auc))
                        
            
            # Save the variables to disk.
#            if epoch % 50 == 0:
#                save_path = saver.save(sess, os.path.join(LOG_DIR, "model.ckpt"))
#                print("Model saved in file: %s" % save_path)
#        save_path = saver.save(sess, os.path.join(LOG_DIR, "model.ckpt"))
#        print("Model saved in file: %s" % save_path)
        print('best auc at epoch: %d, accuracy: %f, AUC: %f' % (best_eval_epoch, best_eval_accuracy, best_eval_auc))
        return best_eval_auc
        
        

def predict(test_data, LOG_DIR_base):
    pred_val_list = []
    
    with tf.Graph().as_default():
        features_pl = tf.placeholder(tf.float32, shape=(None, FEATURE_DIM))
        is_training_pl = tf.placeholder(tf.bool, shape=())
        best_model = dnn_model(features_pl, is_training_pl)
        saver = tf.train.Saver()
        sess = tf.Session()
        
        saver.restore(sess, os.path.join(LOG_DIR_base, "model_best.ckpt"))
        pred_val = sess.run(best_model, feed_dict={features_pl:test_data, is_training_pl:False})
        return pred_val
        
#        for i in xrange(K):
#            saver.restore(sess, os.path.join(LOG_DIR_base+str(i), "model_best.ckpt"))
#            pred_val = sess.run(best_model, feed_dict={features_pl:test_data, is_training_pl:False})
#            pred_val_list.append(pred_val[:, None].copy())
#        return np.mean(np.hstack(pred_val_list) ,axis=1)

def main(unused_argv):
##    print(human.shape) # 1881 1881/5 = 376
##    print(robot.shape) # 98, 98/5 = 19    
    X_train, y_train = prepareTrainData()
    mean = np.mean(X_train, axis=0)
    std = np.std(X_train, axis=0)
    
    X_train = (X_train - mean) / (std + 0.001)        
    tmp = np.hstack([X_train, y_train[:, None]])

    human = tmp[y_train == 0, :] # 1881
    human = human[np.random.permutation(human.shape[0]), :]
    robot = tmp[y_train == 1, :] # 98
    robot = robot[np.random.permutation(robot.shape[0]), :]    
    
    tmp_train_split = np.vstack([human[:-31, :], robot[:-8,:]])
    tmp_eval_split = np.vstack([human[-31:, :], robot[-8:,:]])
    
    eval_data = tmp_eval_split[:, :-1]
    eval_labels = tmp_eval_split[:, -1].astype(np.int32)
    
    print(eval_data.shape)
    print(eval_labels.shape)
    print()
        
    if do_CV:
        CV_human_splits = np.split(tmp_train_split[tmp_train_split[:, -1] == 0], K, axis=0)
        CV_robot_splits = np.split(tmp_train_split[tmp_train_split[:, -1] == 1], K, axis=0)
        score = 0
        for i in xrange(K):
            sub_train_split = np.vstack(CV_human_splits[:i] + CV_human_splits[i+1:] + (CV_robot_splits[:i] + CV_robot_splits[i+1:]))
            sub_hold_out_split = np.vstack([CV_human_splits[i], CV_robot_splits[i]])
            print('Train %dth CV' % i)
            score += train(MAX_EPOCH, sub_train_split[:, :-1], sub_train_split[:, -1], sub_hold_out_split[:, :-1], sub_hold_out_split[:, -1], LOG_DIR_base+str(i))
        score = score / K
        print('Cross validation AUC: %f' % score)
    
        eval_pred = predict(eval_data, LOG_DIR_base)
        new_pred_val = np.argmax(eval_pred, 1)
        eval_accuracy = np.mean(new_pred_val == eval_labels)
        
        normed_pred_val = eval_pred - np.max(eval_pred, axis=1)[:, None]
        probability = np.exp(normed_pred_val[:, 1]) / np.sum(np.exp(normed_pred_val),axis=1)
        eval_auc = roc_auc_score(eval_labels, probability)
        print('Eval accuracy: %f, AUC: %f' % (eval_accuracy, eval_auc))
    
    if do_train:
        train(MAX_EPOCH, tmp_train_split[:, :-1], tmp_train_split[:, -1], eval_data, eval_labels, LOG_DIR_base+'all')
    
    if do_test:    
        common, X_test = prepareTestFeatures()
        X_test = (X_test - mean) / (std + 0.001)
        
        prediction = predict(X_test, LOG_DIR_base+'all')
        print(type(prediction))
        print(prediction.shape)
        prediction = prediction - np.max(prediction, axis=1)[:, None]
        probability = np.exp(prediction[:, 1]) / np.sum(np.exp(prediction),axis=1)

        print(probability[:20])

        predictionDf = pd.DataFrame(data={"prediction": probability})
        pd.concat([common['bidder_id'], predictionDf], axis=1).to_csv(
            "../submissions/{}.csv".format(name),
            index=False,
        )
        
if __name__ == "__main__":
    tf.app.run()        



