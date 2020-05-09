import pymysql
import sqlite3
import threading
import random


class Activity(threading.Thread):
 
    def __init__(self,*details):
        threading.Thread.__init__(self)
        self.details = details
    
    def run(self):
        db_conn = pymysql.connect()
        db_cur = ''
        for i in self.details:
            if 'dict' in str(type(i)):
                mylog = i

                userid = mylog['user']
                time_ = mylog['time']
                desc = mylog['desc']
                act = mylog['activity']
                db_conn = mylog['database']
                db_cur = db_conn.cursor()
                db_cur.execute("insert into user_activity values('{0}','{1}','{2}','{3}')".format(userid,act,time_,desc))
        db_conn.commit()
        db_conn.close()

