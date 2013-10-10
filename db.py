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
    dbcursor.close()
    db.close()
    dbcursor=None
    db=None

def init():
    dbcursor.execute("IF NOT EXISTS DBM CREATE TABLE DBM (name text primary key, fields text); ")
    
def any2str(data):
    if isinstance(data,unicode):
        return data.encode('utf-8') 
    else:
        return str(data) 

def insert_column(tablename,values):
    slist = ','.join(['%s' for i in values])
    sql = "INSERT INTO %s VALUES (%s)" % (any2str(tablename),slist)
    print sql
    print ' '.join(values)
    dbcursor.execute(sql,values)
    db.commit()

def intodb_xls(tablename,file):
    global db,dbcursor
    data=xlrd.open_workbook(file)
    table=data.sheets()[0]
    values = []
    for r in xrange(1,table.nrows):
        for c in xrange(table.ncols):
            values.append(any2str(table.row(r)[c].value))
    print values
    insert_column(tablename,tuple(values))

# fields is a dict
def create_table(name,fields,attrs):

    cmd = "CREATE TABLE " + any2str(name) + "( "
    fnames = []
    values = [name]
    for fn in fields:
        cmd += any2str(fn) + " " + any2str(fields[fn]) + ","
        fnames.append(any2str(fn))
    values.append(','.join(fnames))
    cmd = cmd[:-1] + ");"
    insert_column('DBM',tuple(values))
    dbcursor.execute(cmd)
    db.commit()
