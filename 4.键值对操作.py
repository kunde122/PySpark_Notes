# coding=utf-8
"""
第四章:键值对操作
键值对RDD是Spark中需要的常见数据类型,本章介绍如何操作键值对RDD
键值对RDD通常用来进行聚合计算.一般我们要先通过一些初始ETL操作来讲数据转化为键值对形式.
"""
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("MyApp")
sc = SparkContext(conf=conf)

lines = sc.textFile('C:\\Code\\Python\\Data\\Tmp\\5000-8.txt')
# 4.1动机:为键值对类型的RDD提供了一些专用的操作,这些RDD被称为pair RDD
# 4.2创建Pair RDD
# 在Python中,为了让提取键之后的数据能够在函数中使用,需要返回一个由二元组组成的RDD
pairs = lines.map(lambda x: (x.split(" ")[0], x))
# 当从内存中创建pair RDD时,只需要对这个由二元组组成的集合调用sc.parallelize()方法

# 4.3 Pair RDD的转化操作
# Pair RDD可以使用所有标准RDD上的可用的转化操作
result = pairs.filter(lambda x: len(x[1]) < 20)
# 4.3.1 聚合操作
rdd1 = sc.parallelize([(1, 2), (2, 3), (3, 4), (1, 5), (2, 6), (3, 7)])
rdd2 = rdd1.mapValues(lambda x: (x, 1))
rdd3 = rdd2.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
print rdd3.collect()
# 用python实现单词计数
rdd = sc.textFile(r"C:\Code\Python\Data\MyFather.txt")
words = rdd.flatMap(lambda x: x.split(" "))
results = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)

results2 = rdd.flatMap(lambda x: x.split(' ')).countByValue()  # 一步实现计数

results3 = words.combineByKey((lambda x: (x, 1)),
                              (lambda x, y: (x[0] + y, x[1] + 1)),
                              (lambda x, y: (x[0] + y[0], x[1] + y[1])))  # ???
results3_ = results3.map(lambda key, xy: (key, xy[0] / xy[1])).collectAsMap()
# 并行度调优
# 4.3.2数据分组add.groupByKey()
# 4.3.3连接:内连接join,leftOuterJoin左外连接,rightOuterJoin右外连接,交叉连接
# 4.3.4数据排序rdd.sortByKey(ascending=True,numPartitions=None,keyfunc=lambda x: str(x))
# 4.4Pair RDD的行动操作
# 4.5数据分区(进阶)
