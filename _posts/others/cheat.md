author: Kai Zhang
title: Programmer's cheatsheet
date: 2015-04-06

--begin--

# Programmer's Cheatsheet

## find

| command | description |
| ------- | ----------- |
| find . -newermt "2015-03-10 0023" -not -newermt "2015-03-10 0024" | 查找一段时间内的文件 |

## git

| command | description |
| ------- | ----------- |
| git daemon --export-all --base-path=.. --enable=receive-pack | Create a simple temporary git server |

## nc

| command | description |
| ------- | ----------- |
| nc ip port | connect to ip on port |
| nc -uvl localhost port | receive message that sends to localhost on port |

## netstat

| command | description |
| ------- | ----------- |
| netstat -apn | 查看已占用的端口 |

## printenv

| command | description |
| ------- | ----------- |
| printenv | Prints the list of environment variables |

## rsync

| command | description |
| ------- | ----------- |
| rsync -r source target | 将source文件夹同步到target内 |
| rsync -r source/ target | 将source内部文件同步到target内 |

## tar

| command | description |
| ------- | ----------- |
| tar zcf files.tar.gz file1 file2 | 压缩 |
| tar zxf files.tar.gz | 解压 |

*  -v 详细 
