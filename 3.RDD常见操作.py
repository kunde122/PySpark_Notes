# coding=utf-8
"""
在python中初始化spark
"""
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("MyApp")
sc = SparkContext(conf=conf)

lines = sc.textFile('C:\\Code\\Python\\Data\\Tmp\\5000-8.txt')
pythonLines = lines.filter(lambda line: 'a' in line)
print pythonLines.first()
# 如果想多次调用pythonLines，则可将其写入内存中
pythonLines.persist()
print pythonLines.count()
# 常见的转化操作和行动操作
# 1.基本RDD
# 1.1针对各个元素的转化操作：map,flatmap, filter
nums = sc.parallelize([1, 2, 3, 4])
squared = nums.map(lambda x: x ** 2).collect()
print squared

lines = sc.parallelize(['hello world', 'hi i am fine'])
words = lines.map(lambda x: x.split(' ')).collect()
word_ = lines.flatMap(lambda x: x.split(' ')).collect()  # 每个输入元素生成多个输出元素
print words
print word_
# 1.2伪集合操作：尽管RDD本身不是严格意义上的集合，但是支持很多集合操作，这些操作要求RDD是相同的数据类型
collector = sc.parallelize([1, 1, 2, 3, 4, 2])
print collector.distinct().collect()  # 去重，开销很大，因为用到了数据混洗
print collector.union(collector).collect()  # 将两RDD的所有元素放到一个RDD中
# 返回两个RDD种都有的元素，开销很大，用到了数据混洗
print collector.intersection(sc.parallelize([1, 2, 4])).collect()
# 返回在第一个不在第二个的所有元素组成的RDD，也需要数据混洗
print collector.subtract(sc.parallelize([1, 2, 3])).collect()
print collector.cartesian(collector).collect()  # 计算两个RDD的笛卡尔积

# 1.3行动操作：reduce,fold,aggregate
sum = sc.parallelize(range(10)).reduce(lambda x, y: x + y)
ji = sc.parallelize(range(1, 10, 1)).reduce(lambda x, y: x * y)  # 累加
ji2 = sc.parallelize(range(10)).fold(1000, lambda x, y: x + y)  # 带初始值的累加

sumCount = nums.aggregate(
    (0, 0),
    (lambda acc, value: (acc[0] + value, acc[1] + 1)),
    (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])))
print('平均值=%s' % (sumCount[0] / float(sumCount[1])))
"""
RDD的一些行动操作会以普通集合或者值得形式将RDD的部分或全部数据返回驱动器程序中
最简单的方式是collect(),collect()通常在单元测试中使用,要求所有数据必须能一同放入单台机器的内存中
take(n)返回RDD中的n个元素,并且尝试只访问尽量少的分区
如果为数据定义了顺序,可以使用top(n)获取前几个元素,top()会使用数据的默认顺序,但我们也可以提供自己的比较函数来提取前几个元素
有时需要对数据采样,takeSample(withReplacement,num,seed)函数可以让我们采样并指定是否替换
有时需要对所有元素应用一个行动操作,但不许任何结果返回驱动器程序中,foreach(f)对每个元素进行操作且不需要把RDD发回本地
"""
# 3.6持久化(缓存)persist()
"""
若简单的对RDD调用行动操作,Spark每次都会重算RDD以及他的所有依赖.这在迭代算法中消耗格外大
为了避免多次计算同一个RDD,可以让Spark对数据进行持久化.当Spark持久化一个RDD时,计算出RDD的节点会分别保存他们所求出的分区数据.如果一个
有持久化数据的借点发生故障,Spark会再需要用到的缓存的数据时重算丢失的数据分区.如果希望节点故障的情况不会拖累我们的执行速度,
也可以把数据备份到多个节点上
在Python中,我们会始终序列化要持久化存储的数据
最后RDD还有一个方法叫做unpersist() 使用该方法可以手动把持久化的RDD从缓存中移除
"""
sum.persist()
