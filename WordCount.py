# coding=utf-8
"""
@author: XiLin Chen
@date: 2017/01/20 09:06
"""
from pyspark import SparkContext, SQLContext, SparkConf


def create_spark_context():
    conf = SparkConf().setAppName('WordCount').set('spark.ui.showConsoleProgress', 'false')  # 设置不要显示Spark执行进度
    sc = SparkContext(conf=conf)
    print 'master=%s' % sc.master  # 显示目前执行的模式,local,Yarn client,Spark Stand alone
    set_logger(sc)
    set_path(sc)
    return sc


def set_logger(sc):
    """设定不要显示太多信息"""
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger('org').setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger('akka').setLevel(logger.Level.ERROR)
    logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)


def set_path(sc):
    """设定文件读取路径"""
    global Path
    if sc.master[0:5] == 'local':
        Path = 'file:C:\\Code\\Python\\Data\\test.txt'
    else:
        Path = 'hdfs://localhost:9001/Input/test.txt'


if __name__ == '__main__':
    print '开始程序RunWordCount'
    sc = create_spark_context()
    print '开始读取数据'
    text_file = sc.textFile(Path)
    print Path
    counts_rdd = text_file.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
    print counts_rdd.collect()
    counts_rdd.saveAsTextFile('file:C:\\Code\\Python\\Data\\test_out.txt')
    print 'end'
