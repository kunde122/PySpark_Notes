# coding=utf-8
"""MLlib决策树二元分类
@Author: XiLin Chen
@Date: 2017-03-08 15:41
"""
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint
import numpy as np

conf = SparkConf().setMaster('local').setAppName('dicision_tree')
sc = SparkContext(conf=conf)
print(sc.master)

# -------------------------------------------------------------------------------------------------------------------- #
# 1.读取并转换数据
# 1.1 设定文档读取路径
# if sc.master[:5] == 'master':
#     Path = 'hdfs://localhost:9001/data'
# else:
#     Path = 'C:\Code\ML\Pyspark\decision_tree\data'
Path = 'hdfs://localhost:9001//'

# 1.2 读取文档并查看数据
rawDataWithHeader = sc.textFile(Path + 'data//train.tsv')
print(rawDataWithHeader.take(2))

# 1.3处理文档(\t分开)
header = rawDataWithHeader.first()  # 数据的header, 即字段名
rawData = rawDataWithHeader.filter(lambda x: x != header)  # 非字段名的其他数据, 用函数filter筛选
rData = rawData.map(lambda x: x.replace('\"', ''))  # 将文档里的\"删除
lines = rData.map(lambda x: x.split('\t'))
print('共计: %s行' % lines.count())

# -------------------------------------------------------------------------------------------------------------------- #
# 2.提取特征栏位
# 2.1 建立extract_features函数, 用来提取特征栏位


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


# -------------------------------------------------------------------------------------------------------------------- #
# 3.提取分类特征栏
# 数据的第三(从零开始计数)列是离散分类型数据, 需要将其转为数值型方可计算
# 此处采用OneHotEncoder方式: 如果有N个分类, 则转化成N个数值栏位, 具体步骤如下:

# 3.1 建立categoriesMap网页分类字典
categoriesMap = lines.map(lambda fields: fields[3]).distinct().zipWithIndex().collectAsMap()
print(categoriesMap)

# 3.2 提取分类特征栏位
# categoryIdx = categoriesMap[field[3]]

# -------------------------------------------------------------------------------------------------------------------- #
# 4.提取数字特征栏位
# 因为很多资料没有数值会以?代替, 则我们需要将?转为0, 其他的float之--见函数convert_float

# -------------------------------------------------------------------------------------------------------------------- #
# 5.提取label标签栏位


def extract_label(field):
    """提取label栏位, 即每行的最后一位"""
    return float(field[-1])


# -------------------------------------------------------------------------------------------------------------------- #
# 6.建立训练评估所需数据
# 进行Decision Tree的训练, 必须提供LabeledPoint格式的数据, 所以我们先建立LabeledPoint数据

# 6.1 建立LabeledPoint数据
# 之前已经建立了extract_label()与extract_features()函数, 接下来利用这两个函数建立所需的LabeledPoint
labelPointRDD = lines.map(lambda r: LabeledPoint(extract_label(r), extract_features(r, categoriesMap, len(r) - 1)))

labelPointRDD.first()
# 6.2 以随机的方式将数据分为三部分8:1:1
# 利用RDD的randomSplit函数随机分割数据
trainData, validationData, testData = labelPointRDD.randomSplit([8, 1, 1])
