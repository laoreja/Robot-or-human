from commons import *
import math

name = "GDA"


class GDAEstimator():

    def get_params(self, deep=False):
        return {}

    def fit(self, X, y):
        m = y.size
        self.phi = np.count_nonzero(y) * 1. / m
        self.mu0 = np.zeros(X.shape[1])
        self.mu1 = np.zeros(X.shape[1])
        for i in range(m):
            if y[i] > 0:
                self.mu1 += X[i]
            else:
                self.mu0 += X[i]
        self.mu0 *= 1. / m
        self.mu1 *= 1. / m
        sigma = np.zeros([X.shape[1], X.shape[1]])
        for i in range(m):
            cur = X[i] - self.mu1 if y[i] > 0 else X[i] - self.mu0
            for j in range(X.shape[1]):
                sigma[j] += cur[j] * cur
        sigma *= 1. / m
#        print sigma
        self.sigmaInverse = np.linalg.inv(sigma)
        return self

    def predict(self, X):
        results = []
        for x in X:
            logp1 = np.log(self.phi) \
                - 0.5 * (x - self.mu1).dot(self.sigmaInverse).dot(x - self.mu1)
            logp0 = np.log(1 - self.phi) \
                - 0.5 * (x - self.mu0).dot(self.sigmaInverse).dot(x - self.mu0)
            results.append(1 if logp1 > logp0 else 0)
        return results

    def predict_proba(self, X):
        results = np.zeros([X.shape[0], 2])
        for i, x in enumerate(X):
            logp1 = np.log(self.phi) \
                - 0.5 * (x - self.mu1).dot(self.sigmaInverse).dot(x - self.mu1)
            logp0 = np.log(1 - self.phi) \
                - 0.5 * (x - self.mu0).dot(self.sigmaInverse).dot(x - self.mu0)
            p0 = math.exp(logp0)
            p1 = math.exp(logp1)
            if p0 < 1e-5 and p1 < 1e-5:
                p0 = p1 = 0.5
            results[i, 0] = p0 / (p0 + p1)
            results[i, 1] = p1 / (p0 + p1)
        return results


if __name__ == "__main__":
    gda = GDAEstimator()
    featureList = [
        'tdiff_min', 'response_min', 'tdiff_median'
    ]
    X_train, y_train = prepareTrainData(featureList)
    evaluateClassifier(gda, X_train, y_train, name)
    printSubmission(gda, X_train, y_train, name, featureList)
