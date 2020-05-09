import pymysql
import socket
import time
import threading
import sqlite3
import random

class Report(threading.Thread):

    def __init__(self,soc,db_conn,db_cur):
        threading.Thread.__init__(self)
        self.db_conn = db_conn
        self.db_cur = db_cur
        self.soc = soc
    
    def run(self):
        pass

