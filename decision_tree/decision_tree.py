# coding=utf-8
"""MLlib dicision_tree 二元分类
@Author: XiLin Chen
@Date: 2017-03-08 18:10
"""
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.mllib.evaluation import BinaryClassificationMetrics
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
import numpy as np

conf = SparkConf().setMaster('local').setAppName('dicision_tree')
sc = SparkContext(conf=conf)


def PrepareData():
    """
    数据预处理
        Return:
            trainData, validationData, testData, categoriesMap
    """
    global Path
    Path = 'hdfs://localhost:9001//'
    print('开始读取数据')
    rawDataWithHeader = sc.textFile(Path + 'data//train.tsv')
    header = rawDataWithHeader.first()  # 数据的header, 即字段名
    rawData = rawDataWithHeader.filter(lambda x: x != header)  # 非字段名的其他数据, 用函数filter筛选
    rData = rawData.map(lambda x: x.replace('\"', ''))  # 将文档里的\"删除
    lines = rData.map(lambda x: x.split('\t'))
    print('共计: %s行' % lines.count())

    categoriesMap = lines.map(lambda fields: fields[3]).distinct().zipWithIndex().collectAsMap()
    labelPointRDD = lines.map(lambda r: LabeledPoint(
        extract_label(r), extract_features(r, categoriesMap, len(r) - 1)))
    trainData, validationData, testData = labelPointRDD.randomSplit([8, 1, 1])
    print('将数据分为trainData: %s  validationData: %s  testData: %s') % \
        (trainData.count(), validationData.count(), testData.count())
    return trainData, validationData, testData, categoriesMap


def extract_label(field):
    """提取label栏位, 即每行的最后一位"""
    return float(field[-1])


def extract_features(field, categoriesMap, featureEnd):
    """
        Parameters:
            field: 每一行数据
            categoriesMap: categoriesMap字典
            featureEnd: featureEnd 提取特征栏位的结尾位置的索引

        Return:

    """
    # 提取分类特征栏位
    categoryIdx = categoriesMap[field[3]]
    categoryFeatures = np.zeros(len(categoriesMap))
    categoryFeatures[categoryIdx] = 1  # 巧妙的利用索引值将对应的栏位标 1, 则每个分类的特征栏位将转为一个01列表

    # 提取数值栏位
    numericalFeatures = [convert_float(f) for f in field[4: featureEnd]]

    # 返回分类特征栏位 + 数值特征栏位
    return np.concatenate(categoryFeatures, numericalFeatures)  # 合并两个列表的函数


def convert_float(x):
    return (0 if x == '?' else float(x))


def PredictData(model, categoriesMap):
    """
    预测模型
    """
    print('开始读取数据...')
    rawDataWithHeader = sc.textFile(Path + 'data//test.csv')
    header = rawDataWithHeader.first()
    rawData = rawDataWithHeader.filter(lambda x: x != header)
    rData = rawData.map(lambda x: x.replace('\"', ''))
    lines = rData.map(lambda x: x.split('\t'))
    print('共计%s行记录' % lines.count())
    dataRDD = lines.map(lambda r: (r[0], extract_features(r, categoriesMap, len(r))))
    DescDict = {0: '暂时性网页(ephemeral)', 1: '长青网页(evergreem)'}
    for data in dataRDD.take(10):
        predictResult = model.predict(data[1])
        print('网址: %s\n==>预测: %s\n说明: %s' % (data[0], predictResult, DescDict[predictResult]))


def evaluateModel(model, validationData):
    """
    模型评估AUC
    """
    score = model.predict(validationData.map(lambda p: p.feature))
    scoreAndLabels = score.zip(validationData.map(lambda p: p.label))  # [(s1, l1), (s2, l2), ...]
    metrics = BinaryClassificationMetrics(scoreAndLabels)
    AUC = metrics.areaUnderROC
    return AUC


if __name__ == '__main__':
    trainData, validationData, testData, categoriesMap = PrepareData()
    trainData.persist()
    validationData.persist()
    testData.persist()

    # 训练模型
    model = DecisionTree.trainClassifier(
        trainData, numClass=2, catrgoricalFeaturesInfo={}, impurity='entropy', maxDepth=5, maxBins=5)

    # 预测模型
    PredictData(model, categoriesMap)

    # 模型准确率评估
    AUC = evaluateModel(model, validationData)
    print('AUC = %s' % AUC)
