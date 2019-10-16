定义纯python方法会降低程序的速度，因为spark会在python解释器和jvm之间来回切换，要尽可能使用spark的内置功能

rdd.distinct()是一个高消耗的方法，慎用

python rdd 和 scala的主要区别就是，python rdd慢很多, scala速度差不多是python的两倍。。
但当转换到DataFrame上的操作时，python和scala相差无几
但是，需要注意的是，pyspark的DataFrame会快很多，也有一些例外，如python udf的使用，会导致在python和jvm之间来回通讯。
而来回通信，就是最耗时的，尽量避免

Spark DataFrame是Dataset[Row]的一个别名，Row是一个通用的非类型化JVM对象。Dataset是一个强类型的JVM对象集合，通过Scala或者
Java定义的案例类决定。最后一点尤为重要，因为这意味着由于缺乏类型增强的优势，pyspark不支持Dataset API。注意，对于pyspark中不支持的Dataset API
，可以通过转化为RDD或者使用UDF来访问。

from pyspark.sql.functions import *
DataFrame添加一列唯一且递增的id列：df.withColumn('id', monotonically_increasing_id())


