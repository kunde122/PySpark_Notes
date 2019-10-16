# coding=utf-8
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql.types import *

conf = SparkConf().setMaster("local").setAppName("MyApp")

sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
data = sc.textFile('hdfs://localhost:9001/Input/Input_CampusSmartCard/LSJL.txt')
data = data.map(lambda x: x.split('\t'))
schema = ['LSH', 'KH', 'JYLX', 'JYDM', 'SH', 'ZD', 'POS', 'SHMC', 'FSDD', 'JYE', 'YE', 'YJSJ', 'CJSJ', 'RZRQ', 'ID']
# schema = StructType([StructField('LSH', IntegerType(), True)]
data = sqlContext.createDataFrame(data, schema)  # spark数据框,支持sql查询
data.registerTempTable('data')
data.show(n=100)  # 查看100行记录
sqlContext.sql('select JYE from data limit 10').show()
describe_JYE = sqlContext.sql('select max(JYE) MAX, min(JYE) MIN, count(JYE) COUNT, sum(JYE) SUM from data').toPandas()
