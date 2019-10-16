from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
# 两种初始化方式都可以

# 1、SparkSession
spark = SparkSession.builder.master('local').appName('app').getOrCreate()
sc = spark.sparkContext


# 2、SparkContext
conf = SparkConf().setMaster('master').setAppName('app')
sc2 = SparkContext(conf)

spark.read.text()