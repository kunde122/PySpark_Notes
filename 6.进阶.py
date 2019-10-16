# coding=utf-8
from pyspark import SparkContext, SparkConf
import math

conf = SparkConf().setMaster("local").setAppName("MyApp")
sc = SparkContext(conf=conf)
# 6.6数值RDD的操作
"""
status()        count+mean+stdev+max+min
count()         RDD中的元素个数
mean()          平均值
sum()           求和
max()           最大值
min()           最小值
variance        方差
sampleVariance()采样中的方差
stdev()         标准差
sampleStdev()   采样中的标准差
"""
# 异常值检测
distances = sc.parallelize(['1', '2', '3', '4', '6', '7', '8', '9', '10', '100000'])
distanceNumerics = distances.map(lambda x: float(x))
status = distanceNumerics.stats()
stddev = status.stdev()
mean = status.mean()
reasonableDistances = distanceNumerics.filter(lambda x: math.fabs(x - mean) < 3 * stddev)
print reasonableDistances.collect()
