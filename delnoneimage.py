#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def smail():
    maillist = ['guopengchao@graphstrategist.com', '502302555@qq.com']
    fromaddr = 'guopengchao@graphstrategist.com'
    # 构建 邮件 开头 标题 body
    msg = MIMEMultipart()
    msg['From'] = 'guopengchao@graphstrategist.com'
    msg['to'] = 'dev'
    msg['Subject'] = 'docker none images del email'
    body = 'have del the none images'
    msg.attach(MIMEText(body, 'plain'))
    # 登录邮箱发送邮件 密码部分需要 填写 163 的授权码
    server = smtplib.SMTP('smtp.qiye.163.com')
    server.login("guopengchao@graphstrategist.com", '登录授权码')
    server.sendmail('guopengchao@graphstrategist.com', maillist, msg.as_string())

# shell docker images |grep "<none>" | awk '{ print $3}' output  dockerimgs tag none
# dockerimagetag arg is  iamges tag (镜像 的标签)
def getnoneimagestagandid(dockerimagetag):
    dockernonetag = []
    dockerimagesid = []
    docimgs = os.popen('docker images').readlines()
    for m in docimgs:
        if m.split()[0] != 'REPOSITORY':
            if m.split()[1] == dockerimagetag:
                if dockerimagetag == 'latest':
                    dockernonetag.append(m.split()[0])
                    dockerimagesid.append(m.split()[2])
                else:
                    dockernonetag.append(m.split()[0] + ':' + m.split()[1])
                    dockerimagesid.append(m.split()[2])
    return dockernonetag, dockerimagesid


# imagetag arg is docker ps -a command output IMAGE
def getcontainerid(imagetag):
    containerlt = []
    containerps = os.popen('docker ps -a ').readlines()
    for n in containerps:
        if imagetag == n.split()[1]:
            containerlt.append(n.split()[0])
    return containerlt


if __name__ == '__main__':
    logfile = open('/upload/delimages.log', 'a+')
    searchimagetag = 'latest'
    if getnoneimagestagandid(searchimagetag)[0]:
        for i in getnoneimagestagandid(searchimagetag)[0]:
            if getcontainerid(i):
                for j in getcontainerid(i):
                    os.system('docker rm ' + j)
            else:
                print >> logfile, "container tag (%s) id is  not exist !" % i
    else:
        print >>logfile, "images tag (%s) is not exist !" % searchimagetag
    for n in getnoneimagestagandid(searchimagetag)[1]:
        os.system('docker rmi ' + n)
    logfile.close()

