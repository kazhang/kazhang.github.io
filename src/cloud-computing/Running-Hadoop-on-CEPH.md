# Hadoop和CephFS整合

## 前提
1. 有一个运行中的CEPH集群，可以参照[CEPH官方指南](http://ceph.com/docs/master/rados/deployment/)安装。
2. 有一个运行中的Hadoop，可以参照[Running Hadoop on Ubuntu Linux (Single-Node Cluster)](http://www.michael-noll.com/tutorials/running-hadoop-on-ubuntu-linux-single-node-cluster/)的步骤。

## 安装必要的包
需要在Hadoop节点上安装的包有：

* libcephfs-java
* libcephfs-jni

安装这两个包需要先添加CEPH的源

    wget -q -O- 'https://ceph.com/git/?p=ceph.git;a=blob_plain;f=keys/release.asc' | sudo apt-key add -
    echo deb http://ceph.com/debian-dumpling/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list
    sudo apt-get update
    sudo apt-get install libcephfs-jni libcephfs-java

## 创建软连接
将`libcephfs_jni.so`添加到Hadoop目录中：

    cd $HADOOP_HOME/lib/native/Linux-amd64-64 (or Linux-i386-32 on 32-bit platform)
    ln -s /usr/lib/jni/libcephfs_jni.so .

## 下载CephFS Hadoop 插件

Hadoop需要一个CephFS插件的支持，可以在[CEPH官方网站](http://ceph.com/download/hadoop-cephfs.jar)下载到。 将插件放入`$HADOOP_HOME/lib/`中

## 创建pool
在CEPH控制节点上创建Hadoop使用的池：

    ceph osd pool create hadoop1 100
    ceph osd pool set hadoop1 size 1 
    ceph mds add_data_pool hadoop1

## 授权Hadoop节点
在Hadoop节点上创建一个文件夹保存CEPH配置和keyring，下面以/etc/ceph为例，注意保证Hadoop用户可读这些文件。    

装有ceph-deploy的节点：

    ceph-deploy admin ${$Hadoop_user}@${Hadoop_node_ip}

Hadoop节点：

    sudo chown -R hduser:hadoop /etc/ceph/

## 更改配置
### core-site.xml
打开conf/core-site.xml，作如下更改：

    <?xml version="1.0"?>
    <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
    
    <!-- Put site-specific property overrides in this file. -->
    
    <configuration>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/app/hadoop/tmp</value>
    </property>
    <property>
        <name>fs.default.name</name>
        <value>ceph://${CEPH_monitor_ip}/</value>
    </property>
    <property>
        <name>ceph.conf.file</name>
        <value>/etc/ceph/ceph.conf</value>
    </property>
    <property>
        <name>ceph.auth.id</name>
        <value>admin</value>
    </property>
    <property>
        <name>ceph.auth.keyring</name>
        <value>/etc/ceph/ceph.client.admin.keyring</value>
    </property>
    <property>
        <name>ceph.data.pools</name>
        <value>hadoop1</value>
    </property>
    <property>
        <name>fs.ceph.impl</name>
        <value>org.apache.hadoop.fs.ceph.CephFileSystem</value>
    </property>
    </configuration>

### 更改hadoop-env.sh
打开`$HADOOP_HOME/conf/hadoop-env.sh`，加入`libcephfs.jar`的位置，一般是`/usr/share/java/libcephfs.jar`

    export HADOOP_CLASSPATH=/usr/share/java/libcephfs.jar
