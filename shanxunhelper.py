import requests
import json
import os

#获取id内容
def get(id):
    url1='http://192.168.1.1/cgi-bin/luci/rpc/uci?auth='+token
    
    getid={
    "method":"get",
    "params":["network", "wan", id],
    }

    getitem=json.loads(requests.post(url1,data=json.dumps(getid)).text)['result']

    return getitem

#获取所有信息
def getall():
    username=get('username')
    password=get('password')
    service=get('service')

    print("username:"+str(username))
    print("password:"+str(password))
    print("service:"+str(service))

#设置id内容
def set(id,content):
    url1='http://192.168.1.1/cgi-bin/luci/rpc/uci?auth='+token

    setid={
        "method":"set",
        "params":["network","wan",id,content]
    }

    setitem=json.loads(requests.post(url1,data=json.dumps(setid)).text)['result']

    return setitem

#设置成移动网
def yidong():
    result1=set("username","")
    result2=set("password","")
    result3=set("service","")

    if(result1 and result2 and result3):
        print("set success")
    else:
        print('error,set again')

#设置成电信网
def dianxin(id):
    result1=set("username","")
    result2=set("password",id)
    result3=set("service","")

    if(result1 and result2 and result3):
        print("set success")
    else:
        print('error,set again')
#重启wan网口（断网的时候用，排除路由器问题）
def restartwan():
    url2='http://192.168.1.1/cgi-bin/luci/rpc/sys?auth='+token

    restartwan={
        "method":"exec",
        "params":["/sbin/ifup wan"]
    }

    re=json.loads(requests.post(url2,data=json.dumps(restartwan)).text)['result']

    if(re==''):
        os.system("echo Reboot success")
    else:
        os.system("echo Reboot failed")
#提交所有设置
def commitsettings():
    url1='http://192.168.1.1/cgi-bin/luci/rpc/uci?auth='+token

    commit={
        "method":"commit",
        "params":["network"]
    }

    commitresult=json.loads(requests.post(url1,data=json.dumps(commit)).text)['result']

    return commitresult
#菜单
def menu():
    print("1.电信改密码")
    print("2.改移动网（晚上断网）")
    print("3.重启网络（掉线的时候用）")
    print("4.获取当前账号密码状态")
    print("5.退出")

#获取token
url0 = 'http://192.168.1.1/cgi-bin/luci/rpc/auth'

data = {
    "method":"login",
    "params":["root","password"]
}

token = json.loads(requests.post(url0,data=json.dumps(data)).text)['result']

#print(token)
while(True):
    menu()
    id=input("input your id:")
    if(id==1):
        password=input("input your password:")
        dianxin(password)
        result=commitsettings()
        print(result)
        restartwan()

    elif(id==2):
        yidong()
        result=commitsettings()
        print(result)
        restartwan()

    elif(id==3):
        restartwan()

    elif(id==4):
        getall()

    elif(id==5):
        break
    
    else:
        print("wrong")
        continue
