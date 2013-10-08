#coding=utf-8

import psycopg2
import xlrd

dbcursor=None
db=None

def connect():
    global db,dbcursor
    db=psycopg2.connect(database='mydb',user='postgres',password='123456')
    dbcursor=db.cursor()
def disconnect():
    global db,dbcursor
    dbcursor.close()
    db.close()
    dbcursor=None
    db=None
def intodb(file):
    global db,dbcursor
    data=xlrd.open_workbook(file)
    table=data.sheets()[0]
    connect()
    print "begin insert" + str(table.nrows)
    for i in range(1,table.nrows):
        cmdstr="insert into book values('"+table.row(i)[0].value+"','"+table.row(i)[1].value+"')"
        print cmdstr
        dbcursor.execute(cmdstr)
    db.commit()
    disconnect()
