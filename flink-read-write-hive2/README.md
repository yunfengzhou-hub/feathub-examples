```shell
docker-compose up -d

docker cp ~/Documents/projects/feathub/dev-spark flink:/root/
docker cp . flink:/root/flink-read-write-hive

python -m pip install /root/dev-spark/python/

feathub_lib_dir=/usr/local/lib/python3.7/site-packages/feathub/processors/flink/lib
# feathub_lib_dir=/Users/yuri/Documents/env/python-venv/feathub-dev/lib/python3.7/site-packages/feathub/processors/flink/lib

flink_lib_dir=/usr/local/lib/python3.7/site-packages/pyflink/lib
# flink_lib_dir=/Users/yuri/Documents/env/python-venv/feathub-dev/lib/python3.7/site-packages/pyflink/lib/

#cp $feathub_lib_dir/hadoop-common*.jar $flink_lib_dir
cp $feathub_lib_dir/flink-connector-hive_*.jar $flink_lib_dir
cp $feathub_lib_dir/hive-exec-*.jar $flink_lib_dir
cp $feathub_lib_dir/antlr-runtime-*.jar $flink_lib_dir
#cp $feathub_lib_dir/commons-logging-*.jar $flink_lib_dir
#
#cp $feathub_lib_dir/*.jar $flink_lib_dir

#cp $feathub_lib_dir/hadoop-common*.jar $FLINK_HOME/lib
cp $feathub_lib_dir/flink-connector-hive_*.jar $FLINK_HOME/lib
cp $feathub_lib_dir/hive-exec-*.jar $FLINK_HOME/lib
cp $feathub_lib_dir/antlr-runtime-*.jar $FLINK_HOME/lib
#cp $feathub_lib_dir/commons-logging-*.jar $FLINK_HOME/lib
#cp ./

#cp $flink_lib_dir/*.jar $FLINK_HOME/lib
#rm $FLINK_HOME/lib/slf4j-log4j12-1.6.1.jar
#rm $FLINK_HOME/lib/log4j-slf4j-impl-2.6.2.jar
#rm $FLINK_HOME/lib/commons-cli-1.2.jar
#
#export HADOOP_CONF_DIR=/root/flink-read-write-hive

mv $FLINK_HOME/opt/flink-table-planner_2.12-1.16.1.jar $FLINK_HOME/lib/flink-table-planner_2.12-1.16.1.jar
mv $FLINK_HOME/lib/flink-table-planner-loader-1.16.1.jar $FLINK_HOME/opt/flink-table-planner-loader-1.16.1.jar

#docker cp ~/Downloads/hadoop-mapred-0.22.0.jar flink:/root/flink-read-write-hive
#cp ./hadoop-mapred-0.22.0.jar $FLINK_HOME/lib
#cp ./hadoop-mapred-0.22.0.jar $flink_lib_dir

export HADOOP_VERSION=2.3.0
export PATH=/opt/hadoop-$HADOOP_VERSION/bin/:$PATH

# Download and extract hadoop binary
cd /opt
curl -O https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf hadoop-$HADOOP_VERSION.tar.gz
export HADOOP_CLASSPATH=`hadoop classpath`

apt-get update && apt-get install -y openjdk-8-jdk
update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java 1070
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre
export PATH=$JAVA_HOME/bin/:$PATH

$FLINK_HOME/bin/stop-cluster.sh && $FLINK_HOME/bin/start-cluster.sh

```

替换/usr/hdp/2.6.5.0-292/hadoop/conf/core-site.xml中的内容，kill datanode和namenode（会自动重启）
