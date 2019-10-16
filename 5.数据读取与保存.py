# coding=utf-8
from pyspark import SparkConf, SparkContext
import json
import csv
import StringIO
from pyspark.sql import HiveContext

conf = SparkConf().setMaster("local").setAppName("MyApp")
sc = SparkContext(conf=conf)

# 5.2.1文本文件
# 1.读取文本文件
input_ = sc.textFile(r"C:\Code\Python\Data\MyFather.txt")
"""Spark 支持读取给定目录中的所有文件，以及在输入路径中使用通配字符
（如 part-*.txt）。大规模数据集通常存放在多个文件中，因此这一特性很有
用，尤其是在同一目录中存在一些别的文件（比如成功标记文件）的时候。"""
# 2.保存文本文件
input_.saveAsTextFile('C:\Code\Python\Data\MyFather2.txt')
# 5.2.2 JSON
data = input_.map(lambda x: json.loads(x))
# 筛选出喜爱熊猫的人并保存为JSON
(data.filter(lambda x: x['lovesPandas']).map(lambda x: json.dumps(x)).saveAsTextFile("1"))

# 5.2.3逗号分隔符和制表符分隔符
# 1.读取csv
inputFile = r'C:\Code\Python\Data\1.csv'


def loadRecord(line):
    """读取一行记录"""
    input = StringIO.StringIO(line)
    reader = csv.DictReader(input, filenames=["name", "favouriteAnimal"])
    return reader.next()


input = sc.textFile(inputFile).map(loadRecord)


# 完整读取csv
def loadRecords(fileNameContents):
    """读取给定文件中的所有记录"""
    input = StringIO.StringIO(fileNameContents[1])
    reader = csv.DictReader(input, filednames=['name', 'favoriteAnimal'])
    return reader


fullFileData = sc.wholeTextFiles(inputFile).flatMap(loadRecords)


# 2.保存csv
def writeRecords(records):
    """写出一些记录"""
    output = StringIO.StringIO()
    writer = csv.DictWriter(output, fieldnames=['name', 'favoriteAnimal'])
    for record in records:
        writer.writerow(record)
    return [output.getvalue()]


outputFile = inputFile
# pandaLovers.mapPartitions(writeRecords).saveAsTextFile(outputFile)

# 5.2.4 SequenceFile
""""""
# 读取sequenceFile
data = sc.sequenceFile(inputFile, "org.apache.hadoop.io.Text", 'org.apache.hadoop.io.IntWritable')
# 保存sequenceFile
data2 = sc.parallelize([('Panda', 3), ('Kay', 6), ('Snail', 2)])
data2.saveAsSequenceFile(outputFile)

# 5.2.5 对象文件
"""对象文件在 Python 中无法使用，不过 Python 中的 RDD 和 SparkContext 支持 saveAsPickleFile()
和 pickleFile() 方法作为替代。这使用了 Python 的 pickle 序列化库。不过，对象文件的
注意事项同样适用于 pickle 文件： pickle 库可能很慢，并且在修改类定义后，已经生产的
数据文件可能无法再读出来"""
# 5.2.6 Hadoop输入输出格式
# 1.读取其他Hadoop输入格式
input2 = sc.hadoopFile(inputFile).map(lambda x, y: (str(x), str(y)))
# 2.保存Hadoop输出格式
input2.saveAsNewAPIHadoopFile(inputFile)
# 3.to do
# 5.3文件系统
# 5.3.1 本地文件系统
rdd = sc.textFile(inputFile)
# 5.3.2 Amazon S3
# 5.3.3 HDFS:只需要将输入输出路径指定为hdfs://master:port/path即可
# 5.4 Spark SQL中的结构化数据,详见第九章
# 5.4.1Apache Hive
"""要把 Spark SQL 连接到已有的 Hive 上，你需要提供 Hive 的配置文件。你需要将 hive-site.
xml 文件复制到 Spark 的 ./conf/ 目录下"""
hiveCtx = HiveContext(sc)
rows = hiveCtx.sql('SELECT name, age FROM users')
firstRow = rows.first()
print firstRow.name
# 5.4.2 JSON
tweets = hiveCtx.jsonFile('tweets.json')
tweets.registerTempTable('tweets')
results = hiveCtx.sql('select user.name, text from tweets')
# 5.5 数据库
# 5.5.1 Java数据库连接:任何支持Java数据库连接的关系型数据库都可以:MySql,Postgre等
# 5.5.2 Cassandra
# 5.5.3 HBase
# 5.5.4 Elasticsearch
