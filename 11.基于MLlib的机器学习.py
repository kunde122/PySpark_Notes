# coding=utf-8
from pyspark import SparkContext, SparkConf
from pyspark import SQLContext
# SQLContext.createDataFrame()
from numpy import array
from pyspark.mllib.linalg import Vectors

conf = SparkConf().setMaster("local").setAppName("MyApp")
sc = SparkContext(conf=conf)

# 11.4数据类型
"""
Vector          数学向量mllib.linalg.Vectors类创建:分为稀疏向量和稠密向量
LabeledPoint    带标签的数据点mllib.regression包含一个特征向量和一个标签(由一个浮点数表示)
Rating          用户对一个产品的评分,在mllib.recommendation包中用于产品推荐
各种Model类      每个Model都是训练算法的结果,一般有一个predict()方法用于对新的数据点或数据点组成的RDD进行预测
"""
# 操作向量Vector类
"""
注意:
    1.向量有两种:稠密向量和稀疏向量.稠密向量把所有维度的值存放在一个浮点数数组中.
        稀疏向量只会把各维度中的非零值存储下来.当最多只有10%的元素非零时,我们通常更倾向于使用稀疏向量
        出于对内存和速度的考虑,这是一种很关键的优化手段
    2.在MLlib中任意地方传递的NumPy数组都表示一个稠密向量,也可以使用mllib.linalg.Vectors类创建其他类型的向量
    3.可以使用Numpy对稠密向量进行操作,也可以把这些操作传给MLlib,这样是为了让MLlib保持在较小规模内
"""
# 创建稠密向量<1.0, 2.0, 3.0>--两种方法
denseVec1 = array([1.0, 2.0, 3.0])
denseVec2 = Vectors.dense([1.0, 2.0, 3.0])
# 创建稀疏向量<1.0, 0.0, 2.0, 0.0>--只能用Vectors.sparse()创建
sparseVec1 = Vectors.sparse(4, {0: 1.0, 2: 2.0})  # 字典创建
sparseVec2 = Vectors.sparse(4, [0, 2], [1.0, 2.0])  # 两个分别代表位置和值的list创建

# 11.5算法:MLlib的主要算法以及它们的输入和输出类型
# 11.5.1特征提取:mllib.feature包
# TF-IDF词频-逆文档频率
# 缩放至平均值为0,标准差为1
from pyspark.mllib.feature import StandardScaler

vectors = [Vectors.dense([-2.0, 5.0, 1.0]), Vectors.dense([2.0, 0.0, 1.0])]
dataset = sc.parallelize(vectors)
scaler = StandardScaler(withMean=True, withStd=True)
model = scaler.fit(dataset)
result = model.transform(dataset)
# 正规化长度为1
from pyspark.mllib.feature import Normalizer

normalizer = Normalizer(p=3.0)
result2 = normalizer.transform(dataset)
# Word2Vec
"""
Word2Vec是一个基于神经网络的文本特征化算法,可以将数据传给许多下游算法
mllib.feature.Word2Vec类引入了该算法
"""

# 11.5.2统计--mllib.stat.Statistics类中提供了几种统计函数可以直接在RDD上使用
"""
Statistics.colStats(rdd)计算由向量组成的RDD的统计性综述,包括每列的最大值最小值平均值和方差
Statistics.corr(rdd,method)计算由向量组成的RDD中的列间的相关矩阵,method须是pearson皮尔森相关或spearman斯皮尔曼相关
Statistics.corr(rdd1,rdd2,method)计算两个RDD的相关矩阵,method同上
Statistics.chiSqTest(rdd)计算由LabeledPoint对象组成的RDD中每个特征与标签的皮尔森独立性测试,
                         返回一个ChiSqTestResult对象,其中有p值,测试统计,每个特征的自由度.特征和标签必须是分类的,即离散值
"""
# 11.5.3分类与回归
"""
分类和回归都会使用MLlib中的LabeledPoint类(在mllin.regression包中)
一个 LabeledPoint 其实就是由一个 label（ label 总是一个 Double 值，
不过可以为分类算法设为离散整数）和一个 features 向量组成
"""
# 线性回归
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.regression import LinearRegressionWithSGD

points = sc.parallelize(LabeledPoint([1, 2, 3], 1))  # 创建LabeledPoint组成的RDD
model = LinearRegressionWithSGD.train(points, iterations=200, intercept=True)
print model.weights, model.intercept
# 逻辑回归
# 支持向量机
# 朴素贝叶斯
# 决策树与随机森林
# 11.5.4聚类
# KMeans

# 11.5.5协同过滤与推荐
# 11.5.6降维
# 1.主成分分析
# 2.奇异值分解
# 11.5.7模型评估
# 11.6
from pyspark.mllib.clustering import KMeans
