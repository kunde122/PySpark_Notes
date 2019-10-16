
<!-- toc orderedList:0 depthFrom:1 depthTo:6 -->

* [1.本机执行pyspark程式](#1本机执行pyspark程式)

<!-- tocstop -->

## 1.本机执行pyspark程式
`pyspark --master local[*]`
local[N]代表在本机执行,使用N个线程, N为*表示全部线程
`sc.master`查看目前的执行模式
