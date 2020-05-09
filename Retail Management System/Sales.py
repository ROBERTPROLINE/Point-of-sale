#Facilitate transactions and logging of transactions

import pymysql
import sqlite3
import threading
import datetime
import time
import socket
import random
import RetailLogger.SalesActivity as Slog
import RetailLogger.TransactionReporter as Tpr

class Sale(threading.Thread):

    def __init__(self,soc,db_conn,db_cur):
        threading.Thread.__init__(self)
        self.soc = soc
        self.db_conn = db_conn
        self.db_cur = db_cur

    def run(self):
        loggdetails  = {}
        gen_id = random.random()
        basket  = str(gen_id)[-6:-1] + 'bskt'
        basket = []

        while True:
            product_id = self.soc.recv(1024)
            product_dt = product_id.decode().split(':')

            for product in product_dt:

                if product != "check-out":
                    print(product)
                    self.db_cur.execute("select * from products where product_id = '{0}' AND count>0".format(product))
                    rzltz = self.db_cur.fetchone()
                    print(rzltz)
                    if rzltz == None:
                        self.db_cur.execute("select product_name from products where product_id = '{0}'".format(product))
                        product_name = self.db_cur.fetchone()
                        self.soc.send(("PRODUCT {0} NO LONGER IN STOCK".format(product_name[0]).encode('ascii')))
                        
                        basket = []
                        self.db_conn.rollback()
                        
                    else:
                        basket.append(rzltz[0])

                if product == "check-out":
                    for produ in basket:
                        self.db_cur.execute("select * from products where product_id = '{0}'".format(produ))
                        count = self.db_cur.fetchone()
                        remaining = int(count[-1])-1
                        
                        self.db_cur.execute("update products set count = '{0}' where product_id = '{1}'".format(remaining,produ))
                        self.db_conn.commit()
                        print(product , ' -: remaining : ', remaining)
                        
                    self.soc.send('Transaction Complete'.encode('ascii'))
					
                    signature = self.soc.recv(1024).decode()
                    #################################
                    loggdetails['time'] = '{}:{}'.format(datetime.datetime.today().hour,datetime.datetime.today().minute)
                    loggdetails['total'] = len(basket)
                    loggdetails['goods'] = basket
                    loggdetails['user'] = signature.split(':')[0]
                    loggdetails['amt'] = signature.split(':')[1]
                    loggdetails['phone'] = signature.split(':')[2]
                    loggdetails['database'] = pymysql.connect('localhost','pythonroot422913','claire6772147','retail_db')
                    #################################
					
                    slog1 = Slog.AddSales(loggdetails)

                    slog1.start()
                    #################################
                    #for transaction report
                    #################################
                    self.db_conn.close()
             
def main():
    s = socket.socket()
    ip = socket.gethostbyname(socket.gethostname())
    port = 1991
    addr = ((ip,port))
    s.bind(addr)

    s.listen(3)

    while True:
        soc, addr = s.accept()
        print(addr)
        db_conn = pymysql.connect('localhost','pythonroot422913','claire6772147','retail_db')
        db_cur = db_conn.cursor()

        newCashier = Sale(soc,db_conn,db_cur)
        newCashier.start()
try:
    main()
except Exception as ex:
    print('Error : during processing')
