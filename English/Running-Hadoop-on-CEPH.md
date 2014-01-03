# Running Hadoop on CEPH

## Dependencies 
1. A running Ceph cluster. Please refer to the [Ceph documentation](http://ceph.com/docs/master/rados/deployment/) for installing Ceph.
2. A Hadoop installation. You can follow the steps [Running Hadoop on Ubuntu Linux (Single-Node Cluster)](http://www.michael-noll.com/tutorials/running-hadoop-on-ubuntu-linux-single-node-cluster/) to install Hadoop.

## Installation
The following packages should be installed on Hadoop nodes:

* libcephfs-java
* libcephfs-jni

To install these packages, you may need to add Ceph source first.

    wget -q -O- 'https://ceph.com/git/?p=ceph.git;a=blob_plain;f=keys/release.asc' | sudo apt-key add -
    echo deb http://ceph.com/debian-dumpling/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list
    sudo apt-get update
    sudo apt-get install libcephfs-jni libcephfs-java

Add `libcephfs_jni.so` to Hadoop directory:

    cd $HADOOP_HOME/lib/native/Linux-amd64-64 (or Linux-i386-32 on 32-bit platform)
    ln -s /usr/lib/jni/libcephfs_jni.so .

Dowload CephFS Hadoop plugin

    cd $HADOOP_HOME/lib
    wget http://ceph.com/download/hadoop-cephfs.jar

## Configuration
Create pools for Hadoop on Ceph admin node:

    ceph osd pool create hadoop1 100
    ceph osd pool set hadoop1 size 1 
    ceph mds add_data_pool hadoop1

Create a folder for Ceph configuration and keyring files on Hadoop nodes. Authorize these nodes:

    ceph-deploy admin ${Hadoop_user}@${Hadoop_node_ip}

On Hadoop nodes, make sure Hadoop user has access to those files:

    sudo chown -R hduser:hadoop /etc/ceph/

Open $HADOOP_HOME/conf/core-site.xml, modify it as following:

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

Open `$HADOOP_HOME/conf/hadoop-env.sh`, add the path of `libcephfs.jar`

    export HADOOP_CLASSPATH=/usr/share/java/libcephfs.jar

## Try it
If everything works fine, you can list the root directory:

    $HADOOP_HOME/bin/hadoop fs -ls /
