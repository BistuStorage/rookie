#coding=utf-8

import psycopg2
import xlrd

dbcursor=None
db=None

datatype = ['integer','numeric','text','data','boolean']

def connect():
    global db,dbcursor
    db=psycopg2.connect(database='mydb',user='postgres')
    dbcursor=db.cursor()

def disconnect():
    global db,dbcursor
    dbcursor.close()
    db.close()
    dbcursor=None
    db=None

def init():
    global db,dbcursor
    dbcursor.execute("CREATE TABLE dbm (name text primary key, fields text);")

def any2str(data):
    if isinstance(data,unicode):
        return data.encode('utf-8')
    else:
        return str(data)

def insert_column(tablename,values):
    global db,dbcursor
    slist=','.join(['%s' for i in values])
    sql="INSERT INTO %s VALUES (%s)" % (any2str(tablename),slist)
    print sql
    dbcursor.execute(sql,values)
    db.commit()

def intodb_xls(tablename,file):
    global db,dbcursor

    cmdstr="SELECT fields FROM dbm WHERE name='%s'" % (any2str(tablename),)
    dbcursor.execute(cmdstr)
    columns=dbcursor.fetchone()
    if not columns:
        return 1 
    columns=columns[0].split(",")
    try:
        data=xlrd.open_workbook(file)
        table=data.sheets()[0]
    except:
        return 2
    if table.ncols!=len(columns):
        return 3
    for r in xrange(1,table.nrows):
        values=[]
        for c in xrange(table.ncols):
            values.append(any2str(table.row(r)[c].value))
        insert_column(tablename,tuple(values))
    return 0

# fields and attrs are  dicts
def create_table(name,fields,attrs):
    cmd="CREATE TABLE "+any2str(name)+"("
    fnames=[]
    values=[name]
    for fn in fields:
        cmd+=any2str(fn)+" "+any2str(fields[fn])+","
        fnames.append(any2str(fn))
    values.append(','.join(fnames))
    attrs['primarykey'] = any2str(attrs['primaykey'])
    if attrs['primarykey'] != '':
        cmd += "PRIMARY KEY(%s)" % attrs['primarykey']
    cmd += ")"
    insert_column('DBM',tuple(values))
    dbcursor.execute(cmd)
    db.commit()
    
def search_all_tables(content):
    global db,dbcursor
    
    cmdstr="SELECT * FROM DBM;"#检索dbm表里面的所有记录表内容
    dbcursor.execute(cmdstr)
    dbmdata=dbcursor.fetchall()
    rtdata={}
    for table in dbmdata:
        tmpdata=search_one_table(table[0],tuple(table[1].split(',')),content)#检索一个表
        if tmpdata:
            rtdata[table[0]]=tmpdata
    if rtdata:
        return rtdata#数据格式:{'表名1':searchonetable返回的list1,'表名2':searchonetable返回的list2...}
    else:
        return None

def search_one_table(tablename,columnnames,content):#参数:表名,元组/列表类型的列名,搜索内容
    global db,dbcursor
   
    #cmdstr="SELECT * FROM "+tablename+" WHERE tokenize("+" || ' ' || ".join(columnnames)+")@@tokenize('"+content+" "+content.lower()+" "+content.upper()+"');"
    #cmdstr="SELECT * FROM "+tablename+" WHERE to_tsvector('chinesecfg',"+" || ' ' || ".join(columnnames)+")@@to_tsquery('chinesecfg','"+content+"');"
    contentlists=content.split()
    for i in range(len(contentlists)):
        contentlists[i]="("+contentlists[i]+")"
    cnlists=list(columnnames)
    for i in range(len(cnlists)):
        cnlists[i]=cnlists[i]+"~*'.*("+"|".join(contentlists)+").*'"
    cmdstr="select * from "+tablename+" where "+" or ".join(cnlists)+";"
    print cmdstr
    dbcursor.execute(cmdstr)#执行检索
    rtdata=[]
    rtdata.append(columnnames)
    rtdata.extend(dbcursor.fetchall())
    if len(rtdata)>1:
        return rtdata#数据格式:[(列1名,列2名...),(列1数据,列2数据...),(列1数据,列2数据...)...]
    else:
        return None

