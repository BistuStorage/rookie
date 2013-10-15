#coding=utf-8

import psycopg2
import xlrd

dbcursor=None
db=None

datatype = ['smallint','integer','bigint','real','numeric','double','serial','bigserial','text','date','time','boolean']
strdatatype=['text']
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
    db.commit()

def any2str(data):
    if isinstance(data,unicode):
        return data.encode('utf-8')
    else:
        return str(data)

def get_table_column_types(tablename):
    global db,dbcursor
    cmdstr="select t.typname from pg_class c , pg_attribute a , pg_type t where c.relname='"+tablename+"' and a.attnum>0 and a.attrelid=c.oid and a.atttypid=t.oid;"
    try:
        dbcursor.execute(cmdstr)
        typelists=dbcursor.fetchall()
        for i in range(len(typelists)):
            typelists[i]=typelists[i][0]
        return typelists
    except:
        return None

def insert_column(tablename,values,typelists):
    global db,dbcursor
    rvalues=list(values)
    for i in range(len(rvalues)):
        for t in strdatatype:
            if t==typelists[i]:
                rvalues[i]="'"+rvalues[i]+"'"
                break
    cmdstr="insert into "+tablename+" values ("+",".join(rvalues)+");"
    try:
        dbcursor.execute(cmdstr)
        return 0
    except:
        print "插入行："+",".join(values)+"失败！"
        return 1

def intodb_xls(tablename,file):
    global db,dbcursor

    rtmessage={}
    rtmessage['errorcode']=0
    rtmessage['rightrownums']=0
    rtmessage['wrongrownums']=0
    cmdstr="SELECT fields FROM dbm WHERE name='%s';" % (any2str(tablename),)
    dbcursor.execute(cmdstr)
    columns=dbcursor.fetchone()
    if not columns:
        rtmessage['errorcode']=1
        return rtmessage
    else:
        columns=columns[0].split(",")
    try:
        data=xlrd.open_workbook(file)
        table=data.sheets()[0]
    except:
        rtmessage['errorcode']=2
        return rtmessage
    if table.ncols!=len(columns):
        rtmessage['errorcode']=3
        return rtmessage
    typelists=get_table_column_types(tablename)
    for r in xrange(1,table.nrows):
        values=[]
        for c in xrange(table.ncols):
            values.append(any2str(table.row(r)[c].value))
        ret=insert_column(any2str(tablename),tuple(values),tuple(typelists))
        if ret==0:
            rtmessage['rightrownums']+=1
        else:
            rtmessage['wrongrownums']+=1
    db.commit()
    return rtmessage

# fields and attrs are  dicts
def create_table(name,fnames,fattrs,attrs):
    global db,dbcursor
    #check tablename
    cmdstr="select name from dbm where name='"+any2str(name)+"';"
    try:
        dbcursor.execute(cmdstr)
        rt=dbcursor.fetchall()
        if rt:
            return 2            #table exists
    except:
        return 1                #db error
    #check pk
    pk = attrs['PK']
    pklist=pk.split(',')
    flag=0
    for pl in pklist:
        for fn in fnames:
            if pl==fn:
                flag+=1
                break
    if flag!=len(pklist):
        return 3                #pk must be made of one or more columns
    cmd="CREATE TABLE "+any2str(name)+"("
    for i in range(len(fnames)):
        cmd+=any2str(fnames[i])+" "+any2str(fattrs[i])+","
    cmd += "PRIMARY KEY(%s)" % any2str(pk)+");"
    try:
        dbcursor.execute(cmd)
        typelists=get_table_column_types('dbm')
        values=[name]
        values.append(",".join(fnames))
        insert_column('DBM',tuple(values),tuple(typelists))
        db.commit()
    except:
        db.rollback()
        return 1
    return 0
    
def search_all_tables(content):
    global db,dbcursor
    content = any2str(content)
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
    cmdstr="SELECT * FROM "+tablename+" WHERE to_tsvector('chinesecfg',"+" || ' ' || ".join(columnnames)+")@@to_tsquery('chinesecfg','"+content+"');"
    '''
    contentlists=content.split()
    for i in range(len(contentlists)):
        contentlists[i]="("+contentlists[i]+")"
    cnlists=list(columnnames)
    print cnlists
    for i in range(len(cnlists)):
        cnlists[i]=cnlists[i]+"~*'.*("+"|".join(contentlists)+").*'"
    cmdstr="select * from "+tablename+" where "+" or ".join(cnlists)+";"
    '''
    dbcursor.execute(cmdstr)#执行检索
    rtdata=[]
    rtdata.append(columnnames)
    rtdata.extend(dbcursor.fetchall())
    if len(rtdata)>1:
        return rtdata#数据格式:[(列1名,列2名...),(列1数据,列2数据...),(列1数据,列2数据...)...]
    else:
        return None

