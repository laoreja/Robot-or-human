import matplotlib.pyplot as plt

results = [
    {
        "name": "DT",
        "pattern": "d-b",
        "AUCs":  [0.74878793422776346, 0.80129638162352612, 0.75645202319645843, 0.64235558680037941, 0.6710618252247369, 0.67502563581334418, 0.71390587590911136, 0.71306641595518816, 0.72224920382165603, 0.72916683606631438, 0.73337065772236532, 0.7283141629398745, 0.73411034128382346, 0.72671841825902339, 0.72931641595518815, 0.72050444391742341, 0.73150839092921349, 0.72188959660297247, 0.71730343994217827, 0.71762702150246183, 0.69892191240908885, 0.69827418462302937, 0.69253732438903193, 0.69577040136423174, 0.68614878371052979, 0.71108890093508603, 0.67573268170935541, 0.67014257803677091],
    },
    {
        "name": "LR",
        "pattern": "x-r",
        "AUCs": [0.89713955989971539, 0.900475609274066, 0.90322658896869501, 0.90526188056195511, 0.90345252857207392, 0.89949610380810407, 0.8907021107196097, 0.88861677282377927, 0.88452009079821114, 0.88309133464335721, 0.85540195713059597, 0.84831871979039619, 0.85525874666847368, 0.84486177553417363, 0.82898342142115011, 0.83636913877219132, 0.83905139020644182, 0.84675630731354745, 0.84795689908298311, 0.84784661991236387, 0.84780473867281025, 0.84675839092921357, 0.84209796946289006, 0.8420019593892577, 0.84172796675249595, 0.83181951032208523, 0.82285889574016358, 0.81327205583412376],
    },
    {
        "name": "RF",
        "pattern": "x-g",
        "AUCs": [0.8855624294168134, 0.91882242681935211, 0.93092868274833984, 0.93961302062158381, 0.93897684306816642, 0.94147601300989292, 0.94333353096625561, 0.94694891753625143, 0.94406290655915437, 0.94449535844965449, 0.94487383678908621, 0.9449864762614627, 0.94377447824908522, 0.94371139382030078, 0.94795464606766955, 0.94653825044043916, 0.94715756425893305, 0.93974275816506314, 0.94346803428648873, 0.94265079956633691, 0.94210807132854502, 0.94126399523422322, 0.93728149986448039, 0.93908630065049459, 0.94329129116411448, 0.94129302468717524, 0.93387683233952201, 0.93624313084428779],
    },
    {
        "name": "GBT",
        "pattern": "x-c",
        "AUCs": [0.86842498418936631, 0.89321333909292144, 0.91080119822017436, 0.92761068572977368, 0.93235588889641785, 0.94030801655599228, 0.94248003907485212, 0.94100585275782633, 0.94238961636626462, 0.93973459874870124, 0.93803292564484808, 0.93839496939513034, 0.94065988221077834, 0.9390164487057866, 0.93797412985047646, 0.93188033326557351, 0.93579312915029134, 0.9348137535573926, 0.93175999175588387, 0.93157417728237801, 0.937671220693861, 0.93417878721145597, 0.9318120567375886, 0.93646574739124544, 0.92702642069837826, 0.92680457491981749, 0.92494768374215119, 0.92633456430410632],
    },
    {
        "name": "GDA",
        "pattern": "x-b",
        "AUCs": [0.76329666904842841, 0.81239734313849166, 0.84798183377974734, 0.81193799831952007, 0.80157891980449569, 0.78289701181993221, 0.76998782324490167, 0.72835369463229704, 0.6683748082358506, 0.69688540847997105, 0.79631648776155073, 0.79580324272878833, 0.79716557139925648, 0.80360326092235479, 0.81341533601705951, 0.81411266750589972, 0.8198805747970902, 0.8183814172115893, 0.81276016210369384, 0.80704915123951348, 0.80041500292162793, 0.79278705734596655, 0.78435425257532021, 0.77815627927802866, 0.76844650165484185, 0.77751148149757199, 0.76795318505631049, 0.74901511813191946],
    },
    {
        "name": "RFLR",
        "pattern": ".-r",
        "AUCs": [0.85115249784027613, 0.89296542780691168, 0.92070061809915571, 0.92203261242436019, 0.92772533757794073, 0.93736053484250192, 0.9365888030922942, 0.94288227637873023, 0.94317106239982706, 0.94596712120853088, 0.94127178950212098, 0.94350324158892529, 0.93967734479414622, 0.9347986493635787, 0.93965322151047048, 0.93976636225943511, 0.9392459180068724, 0.92968669143596305, 0.93536598411860927, 0.9335364564554185, 0.93873625533807514, 0.93141261803541209, 0.92631486443298527, 0.93214237205567119, 0.92853805828301406, 0.93039880499237793, 0.92908912401864185, 0.92871276939524228],
    },
    {
        "name": "GBTLR",
        "pattern": ".-g",
        "AUCs": [0.88830541672303176, 0.90800252427865269, 0.92748979321716962, 0.92927207126607858, 0.93096190881229912, 0.93276946947530814, 0.93125533737433797, 0.92967487319055575, 0.93112385780795248, 0.92927351491236254, 0.92881598815578137, 0.9291217652472531, 0.9232777691314169, 0.92167461801509853, 0.92421634499244598, 0.91766025477679503, 0.92239602191586911, 0.92227961913886092, 0.92309291920096537, 0.92116967719657539, 0.92037496278662645, 0.92067327450274561, 0.92307430014625302, 0.92429815669646065, 0.92462733121821028, 0.92126804640239957, 0.91092930615514323, 0.88757939605512304],
    },
    {
        "name": "SVM(RBF)",
        "pattern": ".-c",
        "AUCs": [0.81838714877806384, 0.88821383035189949, 0.90389587850657271, 0.90678931483489189, 0.90844082305642149, 0.90784501626236613, 0.90825009316980621, 0.90923078443330174, 0.9093094141030853, 0.9096977119754257, 0.90957900799566338, 0.90654215510231739, 0.90807616208158293, 0.90722061480778782, 0.90661503930071818, 0.90852026019785892, 0.9082296155757329, 0.9076565478610471, 0.90628623458463209, 0.90542727673126433, 0.90358623853729048, 0.89985215081085967, 0.89530798549939028, 0.88106331876496369, 0.86676212336811675, 0.85413108144735062, 0.84591128540452643, 0.82703550616614718],
    },
    {
        "name": "RFAda",
        "pattern": ".-b",
        "AUCs": [0.86606886942675154, 0.9275679744319465, 0.93530564496092516, 0.94065051723359083, 0.94255537109816145, 0.943081261010977, 0.94663946108325425, 0.94830340606224883, 0.95081298843565065, 0.94813298719338668, 0.94880686181506069, 0.95174016917378146, 0.94834459276324712, 0.94457272044540819, 0.9476152425802955, 0.94541507713330619, 0.94536380832994538, 0.94712608415774491, 0.94657343757058321, 0.94593127738627636, 0.94356130008582917, 0.94411430523557849, 0.94250377761214266, 0.94119417152278995, 0.94036955662465549, 0.9431849533586304, 0.93878701382301122, 0.93859177508244118],
    },
]

xs = range(len(results[0]["AUCs"]))
plt.xlabel("# of features")
plt.ylabel("Average AUC for CV (K=4)")
for result in results:
    plt.plot(xs, result["AUCs"], result["pattern"], label=result["name"])
lgd = plt.legend(bbox_to_anchor=(1.25, 1.00))
plt.title("Feature Selection for Models")
plt.savefig("./img/feature-selection-all.eps", bbox_extra_artists=(lgd,), bbox_inches='tight')