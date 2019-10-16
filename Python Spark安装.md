
<!-- toc orderedList:0 depthFrom:1 depthTo:6 -->

* [1.环境准备](#1环境准备)
    * [1.首先修改主机名vi /etc/hostname:](#1首先修改主机名vi-etchostname)
    * [2.配置hosts](#2配置hosts)
    * [3.ssh免密码登录](#3ssh免密码登录)
* [2.Java安装](#2java安装)
* [3.scala安装](#3scala安装)
* [4.Hadoop YARN安装配置](#4hadoop-yarn安装配置)
    * [配置Hadoop](#配置hadoop)

<!-- tocstop -->
## 1.环境准备
> 我们将搭建1个master，2个slave的集群方案。

### 1.首先修改主机名vi /etc/hostname:

- 在master上修改为master.hadoop(192.168.200.30:22)
- 其中一个slave上修改为slave1.hadoop(192.168.200.31:22)
- 另一个slave上修改为slave2.hadoop(192.168.200.32:22)

### 2.配置hosts
> 在每台主机上修改hosts vim /etc/hosts
```
    192.168.200.30 master.hadoop
    192.168.200.31 slave1.hadoop
    192.168.200.32 slave2.hadoop
```
> 配置之后ping一下用户名看是否生效
```
    ping slave1.hadoop
    ping slave2.hadoop
```

### 3.ssh免密码登录
> 安装Openssh server
```
    sudo apt-get install openssh-server
```
> 在所有机器上都生成私钥和公钥
```
    ssh-keygen -t rsa   # 一路回车
```
> 需要让机器间都能相互访问，就把每个机子上的id_rsa.pub发给master节点，传输公钥可以用scp来传输。
```
    scp ~/.ssh/id_rsa.pub root@master:~/.ssh/id_rsa.pub.slave1.hadoop
```
> 在master上，将所有公钥加到用于认证的公钥文件authorized_keys中
```
    cat ~/.ssh/id_rsa.pub* >> ~/.ssh/authorized_keys
```
> 将公钥文件authorized_keys分发给每台slave
```
    scp ~/.ssh/authorized_keys spark@slave1:~/.ssh/
```
> 在每台机子上验证SSH无密码通信
```
    ssh master.hadoop
    ssh slave1.hadoop
    ssh slave2.hadoop
```
> 如果登陆测试不成功，则可能需要修改文件authorized_keys的权限（权限的设置非常重要，因为不安全的设置安全设置,会让你不能使用RSA功能 ）
```
chmod 600 ~/.ssh/authorized_keys
```
----
## 2.Java安装

> 从官网下载最新版 Java 就可以，Spark官方说明 Java 只要是6以上的版本都可以，我下的是 jdk-7u75-linux-x64.gz
> 在~/workspace目录下直接解压
```
    tar -zxvf jdk-7u75-linux-x64.gz
```
> 修改环境变量sudo vi /etc/profile，添加下列内容，注意将home路径替换成你的：
```
    export WORK_SPACE=/home/spark/workspace/
    export JAVA_HOME=$WORK_SPACE/jdk1.7.0_75
    export JRE_HOME=/home/spark/work/jdk1.7.0_75/jre
    export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
    export CLASSPATH=$CLASSPATH:.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib
```
> 然后使环境变量生效，并验证 Java 是否安装成功
```
    source /etc/profile   # 生效环境变量
    java -version         # 如果打印出如下版本信息，则说明安装成功
    java version "1.7.0_75"
    Java(TM) SE Runtime Environment (build 1.7.0_75-b13)
    Java HotSpot(TM) 64-Bit Server VM (build 24.75-b04, mixed mode)
```
----
## 3.scala安装
在选择Spark版本时, Spark版本必须和已安装的Hadoop版本兼容
> 我们在master主机上安装Spark(2.1.0版本)

1. 下载Spark安装包http://d3kbcqa49mib13.cloudfront.net/spark-2.1.0-bin-hadoop2.6.tgz
2. tar xvf
3. mv spark-2.1.0 /root/xiligey/install/spark-2.1.0
4. vim .bashrc添加两项
    * export SPARK_HOME=/root/xiligey/install/spark-2.1.0
    * export PATH=$PATH:SPARK_HOME/bin
5. source ~/.bashrc使4生效
----
## 4.Hadoop YARN安装配置
> 官网下载hadoop, 解压并移动至usr/hadoop
```
    tar xvf hadoop-2.5.0.tar.gz
    mv hadoop-2.5.0 /usr/hadoop
```
### 配置Hadoop
> 进入hadoop配置目录(cd /usr/hadoop/etc/hadoop) 需要配置7个文件
`hadoop-env.sh`, `yarn-env.sh`，`slaves`，`core-site.xml`，`hdfs-site.xml`，`maprd-site.xml`，`yarn-site.xml`
> 1. hadoop-env.sh
```
    export JAVA_HOME=/usr/java/jdk1.8.0_101
```
> 2. yarn.sh
```
    export JAVA_HOME=/usr/java/jdk1.8.0_101
```
> 3. slaves
```
    slave1.hadoop
    slave2.hadoop
```
> 4. core-site.xml
```
<configuration>
<property>

  <name>hadoop.tmp.dir</name>

  <value>/usr/hadoop/tmp</value>

  <description>A base for other temporary directories.</description>

  </property>

  <property>

  <name>fs.default.name</name>

  <value>hdfs://master.hadoop:9000</value>

 </property>
</configuration>

```
> 5. hdfs-site.xml
```
<configuration>
        <property>
                <name>dfs.namenode.name.dir</name>
                <value>file:/usr/hadoop/dfs/name</value>
        </property>
        <property>
                <name>dfs.datanode.data.dir</name>
                <value>file:/usr/hadoop/dfs/data</value>
        </property>
        <property>
                <name>dfs.replication</name>
                <value>1</value>
        </property>

    <property>
        <name>dfs.nameservices</name>
        <value>hadoop-cluster1</value>
    </property>
    <property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>master.hadoop:50090</value>
    </property>
    <property>
        <name>dfs.webhdfs.enabled</name>
        <value>true</value>
    </property>

</configuration>

```
> 6. mapred-site.xml
```
<configuration>
 <property>
                <name>mapreduce.framework.name</name>
                <value>yarn</value>
                <final>true</final>
        </property>

    <property>
        <name>mapreduce.jobtracker.http.address</name>
        <value>master.hadoop:50030</value>
    </property>
    <property>
        <name>mapreduce.jobhistory.address</name>
        <value>master.hadoop:10020</value>
    </property>
    <property>
        <name>mapreduce.jobhistory.webapp.address</name>
        <value>master.hadoop:19888</value>
    </property>
        <property>
                <name>mapred.job.tracker</name>
                <value>http://master.hadoop:9001</value>
        </property>
</configuration>

```
> 7. yarn-site.xml
```
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
    <property>
        <name>yarn.resourcemanager.address</name>
        <value>master:8032</value>
    </property>
    <property>
        <name>yarn.resourcemanager.scheduler.address</name>
        <value>master:8030</value>
    </property>
    <property>
        <name>yarn.resourcemanager.resource-tracker.address</name>
        <value>master:8035</value>
    </property>
    <property>
        <name>yarn.resourcemanager.admin.address</name>
        <value>master:8033</value>
    </property>
    <property>
        <name>yarn.resourcemanager.webapp.address</name>
        <value>master:8088</value>
    </property>
</configuration>
```
> 将配置好的hadoop-2.5.0文件夹分发给所有slaves
```
scp -r ~/workspace/hadoop-2.6.0 spark@slave1:~/workspace/

```
> 启动Hadoop: 在master上执行以下操作
```
    cd $HADOOP_HOME
    bin/hadoop namenode -format
    sbin/start-dfs.sh
    sbin/start-yarn.sh
```
> 验证Hadoop是否安装成功:jps命令
```
jps  # run on master.hadoop
3407 SecondaryNameNode
3218 NameNode
3552 ResourceManager
3910 Jps

jps  # run on slaves
2072 NodeManager
2213 Jps
1962 DataNode
```
或者在浏览器输入http://master.hadoop:8088查看hadoop的管理界面
----
## 5.Spark安装
下载解压

进入官方下载地址下载最新版 Spark。我下载的是 spark-1.3.0-bin-hadoop2.4.tgz。

在~/workspace目录下解压

tar -zxvf spark-1.3.0-bin-hadoop2.4.tgz
mv spark-1.3.0-bin-hadoop2.4 spark-1.3.0    #原来的文件名太长了，修改下
配置 Spark

cd ~/workspace/spark-1.3.0/conf    #进入spark配置目录
cp spark-env.sh.template spark-env.sh   #从配置模板复制
vi spark-env.sh     #添加配置内容
在spark-env.sh末尾添加以下内容（这是我的配置，你可以自行修改）：

export SCALA_HOME=/home/spark/workspace/scala-2.10.4
export JAVA_HOME=/home/spark/workspace/jdk1.7.0_75
export HADOOP_HOME=/home/spark/workspace/hadoop-2.6.0
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
SPARK_MASTER_IP=master
SPARK_LOCAL_DIRS=/home/spark/workspace/spark-1.3.0
SPARK_DRIVER_MEMORY=1G
注：在设置Worker进程的CPU个数和内存大小，要注意机器的实际硬件条件，如果配置的超过当前Worker节点的硬件条件，Worker进程会启动失败。

vi slaves在slaves文件下填上slave主机名：

slave1
slave2
将配置好的spark-1.3.0文件夹分发给所有slaves吧

scp -r ~/workspace/spark-1.3.0 spark@slave1:~/workspace/
启动Spark

sbin/start-all.sh
验证 Spark 是否安装成功

用jps检查，在 master 上应该有以下几个进程：

$ jps
7949 Jps
7328 SecondaryNameNode
7805 Master
7137 NameNode
7475 ResourceManager
在 slave 上应该有以下几个进程：

$jps
3132 DataNode
3759 Worker
3858 Jps
3231 NodeManager
进入Spark的Web管理页面： http://master:8080
