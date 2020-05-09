import pymysql
import sqlite3
import threading
import time
import socket
import random

class Sale(threading.Thread):

    def __init__(self,soc,db_conn,db_cur):
        threading.Thread.__init__(self)
        self.soc = soc
        self.db_conn = db_conn
        self.db_cur = db_cur

    def run(self):
        
        data = self.soc.recv(1024)
        product_dt = data.decode()
 
        self.db_cur.execute("select * from products where product_id = '{0}' AND count > 0".format(product_dt))
        rzltz = self.db_cur.fetchone()
        if rzltz == None:
            self.soc.send('PRODUCT NO LONGER IN STOCK'.encode('ascii'))
        else:
            print(rzltz)
            tosend = '{0},{1},{2},{3}'.format(rzltz[1],rzltz[2],rzltz[3],rzltz[4])
            self.soc.send(tosend.encode('ascii'))
       

def main():
    s = socket.socket()
    ip = socket.gethostbyname(socket.gethostname())
    port = 1990
    addr = ((ip,port))
    s.bind(addr)

    s.listen(3)

    while True:
        soc, addr = s.accept()

        db_conn = pymysql.connect('localhost','pythonroot422913','claire6772147','retail_db')
        db_cur = db_conn.cursor()

        newCashier = Sale(soc,db_conn,db_cur)
        newCashier.start()
main()