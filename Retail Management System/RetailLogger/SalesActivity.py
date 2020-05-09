#create and record all sales activity as it takes place
#create backups of all activity as they have happedned before
#backup to be created on csv files and sqlie3 databases
#data to be stored in format favourable for analysis

import pymysql
import threading
import random
import datetime
import time
import sqlite3


class CreateActivity(threading.Thread):

    def __init__(self,*details):
        threading.Thread.__init__(self)
        self.details = details
    
    def run(self):
        db_conn = pymysql.connect()
        db_cur = ''
        for i in self.details:
            if 'dict' in str(type(i)):
                mylog = i
                salestable = mylog['table']

                db_conn = db_conn = pymysql.connect('localhost','pythonroot422913','claire6772147','retail_db')

                db_cur = db_conn.cursor()
                #userid  : sale amt : sale qty : sale time : customer phone
                sql = ("create table {0}(userid varchar(25), sale_value varchar(15), sale_qty varchar(15),time varchar(45), products varchar(1000),customer_phone varchar(15))".format(salestable))
                db_cur.execute(sql)
        db_conn.commit()
        db_conn.close()


class AddSales(threading.Thread):

    def __init__(self,*details):
        threading.Thread.__init__(self)
        self.details = details
    
    def run(self):
        tday = datetime.datetime.today().day
        tyear = datetime.datetime.today().year
        tmonth = datetime.datetime.today().month

        todaes = '{}_{}_{}'.format(tday,tmonth,tyear)

        db_conn = pymysql.connect()
        db_cur = ''

        for i in self.details:
            if 'dict' in str(type(i)):
                mylog = i

                userid = mylog['user']
                amt = mylog['amt']
                qty = mylog['total']
                time = mylog['time']
                cphone = mylog['phone']
                products = str(mylog['goods']).replace(',',':').replace('\'','').replace(']','').replace('[','')
                print(products)
                db_conn = mylog['database']

                db_cur = db_conn.cursor()
                db_cur.execute("insert into {0} values('{1}','{2}','{3}','{4}','{5}','{6}')".format(todaes,userid,amt,qty,time,products,cphone))
            db_conn.commit()



class Backup(threading.Thread):

    def __init__(self,*details):
        threading.Thread.__init__(self)
        self.details = details

    def run(self):
        for i in self.details:
            if 'dict' in str(type(i)):
                bekup = i

                reason = bekup['reason']
                data = bekup['data2bekup']
                #copy all data to sqlite3 databases 
                #copy all data to csv files
        return