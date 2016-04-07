#!/usr/bin/env python
#-*- coding: UTF-8 -*- 

import web  
import functools
import json
import urlparse
import urllib
import random

#URL映射  
urls = (  
        '/beacon/pubkey/', 'beaconPubkey',   
        '/beacon/token/', 'beaconToken',  
        '/client/pubkey', 'clientPubkey',
        '/client/token/', 'clientToken',
        '/client/result/','clientResult'
        )  
app = web.application(urls, globals())  

#模板公共变量  
t_globals = {  
    'datestr': web.datestr,  
    'cookie': web.cookies,  
}  
#指定模板目录，并设定公共模板  
render = web.template.render('templates', base='base', globals=t_globals)  

import mysql.connector

#发送公钥
class beaconPubkey:
	def GET(self):
        conn = mysql.connector.connect(user='root', password='password', database='test', use_unicode=True)#连接数据库
        try:
            cursor = conn.cursor()
        except mysql.connector.errors.OperationalError,e:
            error={'errot_code':3,'error_message':'fail to connect database'}#数据库异常处理
            return jason.dumps(error)
        #获取url中的参数
        data=web.input()
        try:
            beacon_id=data.beacon_id
            pubkey=data.pubkey
            cursor.execute('insert into beacon(beacon_id, pubkey) values (%s,%s)',[beacon_id,pubkey])#向数据库中插入数据
        except AttributeError,e:
            error={'error_code':1,'error_message':'lack of required parameters'}
            return json.dumps(error)
        conn.commit()
        cursor.close()
        conn.close()
        error={'0':'success'}
        return json.dumps(error)
        #return  jsonStr


#获取公钥
class clientPubkey:
    def GET(self):
        conn = mysql.connector.connect(user='root',password='password', db='test', use_unicode = True)
        try:
                cur = conn.cursor()
        except mysql.connector.errors.OperationalError,e:
                error={'errot_code':3,'error_message':'fail to connect database'}
                return jason.dumps(error)
        cur.execute ('select pubkey from beacon order by i desc limit 1')
        pubkey = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return_pubkey = {'pubkey' : pubkey}
        json_pubkey = json.dumps(return_pubkey)
        return json_pubkey

#生成令牌
class clientToken:
    def GET(self):
        conn = mysql.connector.connect(user='root',password='password', db='test', use_unicode = True)
        data=web.input()
        client_id=data.client_id
        if (client_id):
            token = random.randint(100000000, 999999999)  #produce 9-digit random integer
            try:
                cur = conn.cursor()
            except mysql.connector.errors.OperationalError,e:
                error={'errot_code':3,'error_message':'fail to connect database'}
                return jason.dumps(error)
            value = [client_id, token] 
            cur.execute ('insert into client(client_id,token) values(%s,%s)',value)#插入客户端设备记录
            conn.commit()
            cur.close()
            conn.close()
            return_token = {'if_valid' : 'true', 'token' : token}
            json_token = json.dumps(return_token)
            return json_token
        else: 
            return_token = {'if_valid' : 'false'}
            json_token = json.dumps(return_token)
            return json_token

#令牌验证
class beaconToken:
    def GET(self):
        conn = mysql.connector.connect(user='root', password='password', database='test', use_unicode=True,buffered=True)
        try:
            cursor = conn.cursor()
        except mysql.connector.errors.OperationalError,e:
            error={'errot_code':3,'error_message':'fail to connect database'}
            return jason.dumps(error)
        data=web.input()
        #验证令牌是否一致
        try:
            beacon_id=data.beacon_id
            client_id=data.client_id
            token=data.token
        except AttributeError,e:
            error={'error_code':1,'error_message':'lack of required parameters'}
            return json.dumps(error)
        cursor.execute('select  beacon_id from beacon')
        beacon_id0=cursor.fetchall()
        cursor.execute('select  token from client where client_id=%s order by i desc limit 1',[client_id])
        try:
            token0=cursor.fetchone()[0]
        except TypeError,e:
            result='false'
            data={'judge':result}
            return json.dumps(data)
        '''cursor.execute('select  client_id from client order by i desc limit 1')
        client_id0=cursor.fetchone()[0]'''
        f1=(token==token0)#令牌是否一致
        for i in range(len(beacon_id0)):
            if (beacon_id==beacon_id0[i][0]):#beacon_id是否一致
                f2=1
                break
            else: 
                f2=0
        if ((f1==1)&(f2==1)):#都一致时结果才为真
            result='true'
            data={'judge':result}
        else:
            result='false'
            data={'judge':result}
        cursor.execute('insert into result(client_id,result) values (%s,%s)',[client_id,result])#记录验证的结果
        conn.commit()
        cursor.close()
        conn.close()
        jsonStr=json.dumps(data)
        return  jsonStr

#结果返回
class clientResult:
    def GET(self):
        data=web.input()
        id=data.client_id
        conn = mysql.connector.connect(user='root',password='password', db='test', use_unicode = True,buffered=True)
        try:
            cursor = conn.cursor()
        except mysql.connector.errors.OperationalError,e:
            error={'errot_code':3,'error_message':'fail to connect database'}
            return json.dumps(error)
        cursor.execute ('select result from result where client_id=%s order by i desc limit 1',[id])#从数据库中获得验证的结果
        try:
            result = cursor.fetchone()[0]
        except TypeError,e:
            error={'error_code':2,'error_message':'id does not exist'}
            return json.dumps(error)
        conn.commit()
        cursor.close()
        conn.close()
        if(result=='true'):
            judge={'judge':'true'}
        else:
            judge={'judge':'false'}
        return json.dumps(judge)

#返回停车位的使用情况
class clientPark:
    def GET(self):
        id=web.input().client_id
        conn=mysql.connector.connect(user='root',password='password',db='test',use_unicode=True,buffered=True)
        try:
            cursor=conn.cursor()
        except mysql.connector.errors.OperationalError,e:
            error={'error_code':3,'error_message':'fail to connect database'}
            return json.dumps(error)
        cursor.execute('select * from parking where client_id=%s',[id])#判断用户是否已经选择车位
        id0=cursor.fetchone()
        if  id0:
            conn.commit()
            cursor.close()
            conn.close()             
            return json.dumps({'error':'You have already booked a parking space, please don\'t repeate the operation' })
        else :#如果没有则返回空余的车位
            spacedict={}
            #将车位分别标记为T（可使用）和F（未使用）
            cursor.execute('select parking_space from parking where client_id is null ')
            spare=cursor.fetchall()
            for item in spare:
                spacedict[item[0]]="T"
            cursor.execute('select parking_space from parking where client_id is not null')
            unspare=cursor.fetchall()
            for item in unspare:
                spacedict[item[0]]="F"
            conn.commit()
            cursor.close()
            conn.close()
            str1=''
            for i in range(1,4):
                key=i
                str1+=spacedict[key]
                print str1
            return json.dumps(str1)

#选择车位
class  clientSelect:
    def GET(self):
        id=web.input().client_id
        parking=int(web.input().parking)
        conn=mysql.connector.connect(user='root',password='password',db='test',use_unicode=True,buffered=True)
        try:
            cursor=conn.cursor()
        except mysql.connector.errors.OperationalError,e:
            error={'error_code':3,'error_message':'fail to connect database'}
            return json.dumps(error)
        cursor.execute('select client_id from parking where parking_space=%s',[parking])
        parking0=cursor.fetchone()[0]
        if  parking0:
            conn.commit()
            cursor.close()
            conn.close()              
            return json.dumps({'erroor':'The spce is not available,try another'})
        else:
            values=[id,parking]
            cursor.execute('update parking set client_id=%s where parking_space=%s',values) 
            conn.commit()
            cursor.close()
            conn.close()        
            return json.dumps({'parking':'success'})   


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
