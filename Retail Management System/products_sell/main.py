import pymysql
import datetime
import threading
import socket
import random

class Cashier(threading.Thread):

    def __init__(self,soc,db_conn,db_cur):
        threading.Thread.__init__(self)
        self.soc = soc
        self.db_conn = db_conn
        self.db_cur = db_cur


    def run(self):
        req = self.soc.recv(2048)
        req_data = req.decode().split('::')

        req_user = req_data[1]

        if req_data[0] == 'newp':
            while True:
                req_product = self.soc.recv(1024)
                product  = req_product.decode().split('::')
                product_id = product[0]
                self.db_cur.execute("select product_name,product_price,buying_price,product_count from products where bar_code = '{0}'".format(product_id))
                result = self.db_cur.fetchone()
           
 
    def Exit(self):
        self.db_conn.commit()
        self.db_conn.close()



def main():

    s = socket.socket()
    ip = socket.gethostname(socket.gethostbyname())
    port = 1111
    addr = ((ip,port))
    s.bind(addr)

    s.listen(3)

    while True:
        soc, addr = s.accept()

        db_conn = pymysql.connect('localhost','pythonroot422913','claire6772147','retail_db')
        db_cur = db_conn.cursor()

        newCashier = Cashier(soc,db_conn,db_cur)
        newCashier.start()