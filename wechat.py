#!/usr/bin/python2.7
#-*-coding:utf-8 -*-
import requests,sys,json
import urllib3
import os
urllib3.disable_warnings()

reload(sys)
sys.setdefaultencoding('utf-8')

def GetToken(Corpid,Secret):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    Data = {
        "corpid":Corpid,
        "corpsecret":Secret
    }
    r = requests.get(url=Url,params=Data,verify=False)
    Token = r.json()['access_token']
    return Token

def SendMessage(Token,User,Party,Agentid,Subject,Content):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": User,                                 # 企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
        "toparty": Party,                                # 企业号中的部门id，群发时使用。
        "msgtype": "text",                              # 消息类型。
        "agentid": Agentid,                             # 企业号中的应用id。
        "text": {
            "content": Subject + '\n' + Content
        },
        "safe": "0"
    }
    r = requests.post(url=Url,data=json.dumps(Data,ensure_ascii=False),verify=False)
    return r.text


if __name__ == '__main__':
    User = sys.argv[1]                                                              # zabbix传过来的第一个参数
    Subject = sys.argv[2]                                                           # zabbix传过来的第二个参数
    Content = sys.argv[3]                                                          # zabbix传过来的第三个参数
    Party = 3
    Corpid = "ww1673dd4daf87f2b8"                                                   # CorpID是企业号的标识
    Secret = "F6ii_3qbz7wng7LpQPRefufvRrdhklbhLBe4JO47ygo"     # Secret是管理组凭证密钥
    #Tagid = '1'                                                                     # 通讯录标签ID
    Agentid = "1000003"                                                                   # 应用ID
    if "Not supported" in Subject.split(':')[0] or "Unknown" in Subject.split(':')[0] :
        #recordfile = open('/usr/lib/zabbix/alertscripts/zabbixwechat.log', 'a+') 
        #print >> recordfile,'----------------------------------'
	#print >> recordfile, Subject
#    print >> recordfile, User
#    print >> recordfile, Subject
#    print >> recordfile, Content
        #recordfile.close()
	pass
    else:
	Token = GetToken(Corpid, Secret)
    	Status = SendMessage(Token,User,Party,Agentid,Subject,Content)
    	print Status

