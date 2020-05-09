#authentication-server for parcelhandlers
import time
import threading
import socket
import random
import pymysql
import datetime
import RetailLogger.UserActivity as Logg
import RetailLogger.SalesActivity as Slog

exitFlag = 0


class Parcel(threading.Thread):
    pass


class User(threading.Thread):


    def __init__(self,threadID,addr,soc,db_conn,db_cur):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.addr     = addr
        self.soc      = soc
        self.db_conn = db_conn
        self.db_cur = db_cur

    def run(self):
        loggdetails = {}
        loggdetails['time'] = time.ctime()
        loggdetails['activity'] = 'login'
        self.soc.send('login'.encode('ascii'))
        auth_req = self.soc.recv(2028)

        user_cred = auth_req.decode().split('::')
        user_id = user_cred[0]
        user_pwd = user_cred[1]
        loggdetails['user'] = user_id
        print(user_cred)

        self.db_cur.execute("Select * from cashiers where username = '{0}'".format(user_id))
        rzltz = self.db_cur.fetchone()
        
        print(rzltz)

        if rzltz == None:
            loggdetails['desc'] = "Failed to loggin"
            self.soc.send('Authentication Failure \nCheck username or password '.encode('ascii'))
            self.soc.close()
            self.db_conn.close()
        

        elif user_pwd != rzltz[2]:
            loggdetails['desc'] = "Wrong password for loggin"
            self.soc.send('Authentication Failure \nCheck username or password '.encode('ascii'))
            self.soc.close()
            self.db_conn.close()
            

        elif user_pwd == rzltz[2]:
            loggdetails['desc'] = "Loggin success"
            fullname = rzltz[0]
            print('login success')
            self.soc.send(("login-successfull:{0}".format(fullname)).encode('ascii'))
            self.db_conn.close()
        loggdetails['database'] = pymysql.connect('localhost','pythonroot422913','claire6772147','retail_db')
        log = Logg.Activity(loggdetails)
        log.start()
            


def main():
    counter = 0

    soc = socket.socket()
    port = 9912
    ip = '127.0.0.1'
    addr = (ip,port)
    soc.bind(addr)
    soc.listen(3)
    print(addr)

    while True:
        client, addr = soc.accept()
        db_conn = pymysql.connect('localhost','pythonroot422913','claire6772147','retail_db')
        db_cur = db_conn.cursor()
        nextThread = User(counter, str(addr), client,db_conn,db_cur)
        nextThread.start()

tday = datetime.datetime.today().day
tyear = datetime.datetime.today().year
tmonth = datetime.datetime.today().month

slogdetails = {}
slogdetails['table'] = '{}_{}_{}'.format(tday,tmonth,tyear)
slog1 = Slog.CreateActivity(slogdetails)
slog1.start()
main()