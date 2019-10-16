
<!-- toc orderedList:0 depthFrom:1 depthTo:6 -->

* [Q1: 终端运行`spark-shell`, 报错如下:](#q1-终端运行spark-shell-报错如下)
* [Q2: 如何在jupyter notebook中运行pyspark](#q2-如何在jupyter-notebook中运行pyspark)

<!-- tocstop -->

# Q1: 终端运行`spark-shell`, 报错如下:
Caused by: ERROR XSDB6: Another instance of Derby may have already booted the database /metastore_db.

A1:
```
# 找到spark-shell的其他instances
ps -ef|grep spark-shell
# 杀进程
kill -9 spark-shell-process-id(example: kill -9 4848)
# 重新运行spark-shell
spark-shell
```
----
# Q2: 如何在jupyter notebook中运行pyspark

A2:
`PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS="notebook" pyspark`
----
