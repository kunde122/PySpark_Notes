from pyspark import SparkConf, SparkContext, SQLContext
conf = SparkConf().setMaster('local').setAppName('ALS')
sc = SparkContext(conf=conf)
sq = SQLContext(sc)
path = r'hdfs://localhost:9000//input/python_spark_hadoop/u.data'
rawUserData = sc.textFile(path)
rawRatings = rawUserData.map(lambda line: line.split('\t')[:3])
ratingsRDD = rawRatings.map(lambda x: (x[0], x[1], x[2]))
ratingsRDD.take(5)
# 投票数
numRatings = ratingsRDD.count()
# 用户数
numUsers = ratingsRDD.map(lambda x: x[0]).distinct().count()
# 电影数
numMovies = ratingsRDD.map(lambda x: x[1]).distinct().count()

from pyspark.mllib.recommendation import ALS
model = ALS.train(ratingsRDD, 10, 10, 0.01)
print(model)
model.recommendProducts(100, 5)
model.predict(100, 1643)
model.recommendUsers(product=200, num=5)

try:
    model.save(sc, r'file:/home/xiligey/Study/Spark/PythonSparkHadoop/ALSmodel')
except Exception as e:
    print(e)
    print('Model已经存在, 请先删除再存储或者更换目录')

from pyspark.mllib.recommendation import MatrixFactorizationModel
try:
    model_ = MatrixFactorizationModel.load(
        sc, r'file:/home/xiligey/Study/Spark/PythonSparkHadoop/ALSmodel')
except Exception as e:
    print(e)
    print('无法找到模型, 请先训练或者更换目录')
print(model_.predict(9, 200))
