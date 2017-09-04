#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 备份文件.tar.gz按周期删除 按照文件创建时间戳处理
import os
import time
import datetime
filedir = '/home/dockerFiles4Runtime/opt/neo4j/backup/'
files = os.listdir(filedir)


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


if __name__ == "__main__":
	neo4jbackdel = open('/home/allscript/neo4j_backup/neo4jbackdel.log', 'a+')
	for i in files:
		if 'tar.gz' in i or 'graph.db' in i:
			modfilename = filedir + i
			if nowMinusCreateDay(modfilename) >=2:
				print >> neo4jbackdel,  modfilename
				os.system('rm -rf ' + modfilename)	
