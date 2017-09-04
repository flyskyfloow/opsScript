#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 删除30天之前创建的目录
import os
import time
import datetime
dname0 = '/home/hdfs/cacheServer/3F8F0AB80BD24641AD87A616D5810207/binData'
dname1 = '/home/hdfs/cacheServer/57BC9DAB27364875E10000007F000002/binData'


def getdateformat(datestructtimeformat):
    y = int(time.strftime('%Y', datestructtimeformat))
    m = int(time.strftime('%m', datestructtimeformat))
    d = int(time.strftime('%d', datestructtimeformat))
    return y, m, d


def nowMinusCreateDay(filepath):
    # print os.path.abspath(filepath)
    createtime = getdateformat(time.localtime(os.stat(filepath).st_ctime))
    nowdate = getdateformat(time.localtime())
    daynow = datetime.datetime(nowdate[0], nowdate[1], nowdate[2])
    daycreate = datetime.datetime(createtime[0], createtime[1], createtime[2])
    daydiff = (daynow - daycreate).days
    return daydiff


# Directory periodically delete
def oldDirDel(dirpath):
    nowTime = time.ctime()
    logfile = open('/home/zht/cacheserverDel.log', 'a+')
    print >> logfile, nowTime
    files = os.listdir(dirpath)
    for i in files:
        dirName = dirpath + '/' + i
        if os.path.isdir(dirName) and nowMinusCreateDay(dirName) > 30:
            print >> logfile, dirName
            os.system('rm -rf ' + dirName)
    logfile.close()


if __name__ == '__main__':
    oldDirDel(dname1)
    oldDirDel(dname0)
