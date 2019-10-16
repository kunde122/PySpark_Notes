```python
# coding=utf-8
# 1.读取本地文件
from pyspark import SparkContext, SparkConf
conf = SparkConf().setMaster('local').setAppName('MyApp')
sc = SparkContext(conf=conf)
textFile = sc.textFile(r'file:C:\Code\Markdown\Spark\Spark数据读取.md')
# 显示行数
print textFile.count()

# 2.读取HDFS文件
textFile = sc.textFile('hdfs://localhost:9001/Input/Input_CampusSmartCard/LSJL.txt')
# 退出spark
exit()
```
