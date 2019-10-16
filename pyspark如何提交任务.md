```bash
export PATH=/opt/miniconda/bin:$PATH
export PYSPARK_PYTHON=/opt/miniconda3/bin/python3
export PYSPARK_DRIVER_PYTHON=/opt/miniconda3/bin/python3


/usr/bin/spark-submit \
--master yarn \
--deploy-mode cluster \
--driver-memory 4g \
--executor-memory 8g \
--num-executors 7 \
--executor-cores 12 \
--name 20190418 \
/tmp/chenxilin/20190418.py
```

# TODO 各个参数详细说明 todo
master：yarn、cluster、local
driver-memory：
