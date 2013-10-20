#coding=utf-8

import psycopg2
import xlrd
import config
import os
from msg import *

dbcursor=None
db=None

datatype = ['smallint','integer','bigint','real','numeric','double','serial','bigserial','text','date','time','boolean']
strdatatype=['text']

def connect():
    global db,dbcursor
    db=psycopg2.connect(database = config.db ,user = config.user)
    dbcursor=db.cursor()

def disconnect():
    global db,dbcursor
    dbcursor.close()
    db.close()
    dbcursor=None
    db=None

def any2str(data):
    if isinstance(data,unicode):
        return data.encode('utf-8')
    else:
        return str(data)

def get_userinfo(username):
    global db,dbcursor
    #return value:
    #error message,query result
    #first check if error message is ''
    #then check query result if []
    cmdstr="select * from users where username='%s';"%username
    print cmdstr
    dbcursor.execute(cmdstr)
    r=dbcursor.fetchone()
    db.commit()

    try:
        dbcursor.execute(cmdstr)
        r=dbcursor.fetchone()
        db.commit()
    except:
        db.rollback()
        return ERR_DB,[]
    if not r:
        return '',[]
    return '',r

def check_invcod(invcod): 
    global db,dbcursor
    #return value:
    #error message,privilege code
    #first check if error message is null,if is null,then error occur
    #then check if query result is null, if is null,then no invcod
    cmdstr="select privilege from invitation_code where code='%s';"%(invcod)
    print cmdstr
    try:
        dbcursor.execute(cmdstr)
        r=dbcursor.fetchone()
        db.commit()
    except:
        db.rollback()
        return ERR_DB,0
    if not r:
        return '',0
    return '',r[0]

def create_newuser(username,password,privilege,invcod):
    global db,dbcursor
    
    #insert into users
    cmdstr="insert into users(username,password,privilege) values('%s','%s',%s);"%(username,password,privilege)
    print cmdstr
    try:
        dbcursor.execute(cmdstr)
    except:
        db.rollback()
        return ERR_DB
    #delete invcod from invitation_code
    cmdstr="delete from invitation_code where code='%s';"%invcod
    print cmdstr
    try:
        dbcursor.execute(cmdstr)
        db.commit()
    except:
        db.rollback()
        return ERR_DB
    return ''

def check_login(username,password):
    global db,dbcursor
    #return value:
    #error message,privilege
    #check username
    msg,ui=get_userinfo(username)
    if msg!='':
        return msg,0
    elif ui==[]:
        return ERR_NOUSER_OR_PWW,0
    #check password
    passwd=ui[2]
    if passwd!=password:
        return ERR_NOUSER_OR_PWW,0
    return '',ui[3]

def check_register(username,password,invcod):
    global db,dbcursor
    #return value:
    #error message
    #check username
    msg,ui=get_userinfo(username)
    if msg!='':
        return msg
    elif ui!=[]:
        return ERR_USER_EXIST
    #check invcod
    msg,pri=check_invcod(invcod)
    if msg!='':
        return msg
    elif pri==0:
        return ERR_WR_INVCOD
    #create new user
    msg=create_newuser(username,password,pri,invcod)
    if msg!='':
        return msg
    return ''
        
def insert_column(tablename,values,coltyps):
    global db,dbcursor

    rvalues=list(values)
    for i in range(len(rvalues)):
        for t in strdatatype:
            if t==coltyps[i]:
                rvalues[i]="'"+rvalues[i]+"'"
                break
    cmdstr="insert into %s values (%s);"%(tablename,",".join(rvalues))
    print cmdstr
    try:
        dbcursor.execute(cmdstr)
    except:
        print "INSERT COLUNM： %s FAIL !" % (",".join(values))
        return ERR_DB
    return ''

def get_fields_name(tablename):
    flist,msg=get_fields(tablename)
    if msg!='':
        return [],msg
    flist=[ff.split('_')[0] for ff in flist]
    return flist,''

def get_fields(tablename):
    global db,dbcursor
    cmdstr="SELECT fields FROM dbm WHERE name='%s';"%tablename
    print cmdstr
    try:
        dbcursor.execute(cmdstr)
        fields=dbcursor.fetchone()
        db.commit()
    except:
        db.rollback()
        return [],ERR_DB
    if fields:
        fields=fields[0].split(",")
    else:
        fields=[]
    return fields,''

def intodb_csv(tablename,filepath):
    global db,dbcursor
    fields,msg=get_fields(tablename)
    if msg!='':
        return msg
    if fields==[]:
        return ERR_TABLE_NO_EXIST
    try:
        file=open(filepath,"r")
        dbcursor.copy_from(file,tablename,sep=',')
        file.close()
        db.commit()
    except:
        db.rollback()
        return ERR_CSV
    return ''

def intodb_xls(tablename,file):
    global db,dbcursor
    
    fields,msg=get_fields(tablename)
    if msg!='':
        return msg
    if fields ==[]:
        return ERR_TABLE_NO_EXIST
    else:
        coltyps=[]
        for fs in fields:
            coltyps.append(any2str(fs.split('_')[1]))
    #open file
    try:
        data = xlrd.open_workbook(file)
        table=data.sheets()[0]
    except:
        return ERR_FILE_OPEN
    #check table
    if table.ncols!=len(coltyps):
        return ERR_TABLE_COL
    #get data and insert
    nsuc=0
    nfai=0
    for r in xrange(1,table.nrows):
        values=[]
        for c in xrange(table.ncols):
            values.append(any2str(table.row(r)[c].value))
        rt=insert_column(tablename,tuple(values),tuple(coltyps))
        if rt=='':
            nsuc+=1
        else:
            nfai+=1
    db.commit()
    return MSG_TABLE_INSERT % (tablename,any2str(nsuc),any2str(nfai))

def if_table_exists(tablename,metatable):
    global db,dbcursor

    cmdstr="SELECT name FROM %s WHERE name='%s' ;"%(metatable,tablename)
    print cmdstr
    try:
        dbcursor.execute(cmdstr)
        rt=dbcursor.fetchall()
    except:
        db.rollback()
        return ERR_DB
    db.commit()
    if rt:
        return ERR_TABLE_EXIST
    return ''

# fields and attrs are  dicts
def create_table(tablename,fnames,fattrs,attrs):
    global db,dbcursor

    #check tablename
    rt=if_table_exists(tablename,config.DBM)
    if rt!='':#error occur
        return rt
    #check pk
    pk = attrs['PK']
    if pk:#if pk is not null
        pklist=pk.split(',')
        flag=0
        for pl in pklist:
            for fn in fnames:
                if pl==fn:
                    flag+=1
                    break
        if flag!=len(pklist):
            return ERR_PK
    #execute
    cmdstr="CREATE TABLE "+tablename+"("
    for i in range(len(fnames)):
        cmdstr+=fnames[i]+" "+fattrs[i]+","
    if pk:
        cmdstr+="PRIMARY KEY(%s)"%pk
    else:
        cmdstr=cmdstr[:-1]
    cmdstr += ");"
    print cmdstr
    try:
        dbcursor.execute(cmdstr)
    except:
        connect()
        db.rollback()
        return ERR_DB
    typelists=['text','text']
    values=[tablename]#tablename
    values.append(",".join([fnames[i]+"_"+fattrs[i] for i in range(len(fnames))]))#colname_attr
    rt=insert_column('dbm',tuple(values),tuple(typelists))
    if rt!='':
        #insert into dbm fail
        db.rollback()
        return rt
    #create table and insert into dbm must be one
    db.commit()
    return ''

def search_master(content):
    global db,dbcursor

    cmdstr="SELECT * FROM %s;"%config.MDM
    print cmdstr
    try:
        dbcursor.execute(cmdstr)
        mdmdata=dbcursor.fetchall()
        db.commit()
    except:
        db.rollback()
        return None
    rtdata={}
    for table in mdmdata:
        collists=table[1].split(',')
        tmpdata=search_one_table(any2str(table[0]),tuple(collists),content)
        if tmpdata:
            rtdata[table[0]]=tmpdata
        elif tmpdata==None:
            return None
    return rtdata

def search_all_tables(content):
    global db,dbcursor
    #return value:
    #None if db error.
    #{} if no result.
    #rtdata({}type) if there is data.

    cmdstr="SELECT * FROM %s;"%config.DBM
    print cmdstr
    try:
        dbcursor.execute(cmdstr)
        dbmdata=dbcursor.fetchall()
        db.commit()
    except:
        db.rollback()
        return None#db error
    rtdata={}
    for table in dbmdata:
        collists=table[1].split(',')
        for i in range(len(collists)):
            collists[i]=collists[i].split('_')[0]
        tmpdata=search_one_table(any2str(table[0]),tuple(collists),content)#检索一个表
        if tmpdata:
            rtdata[table[0]]=tmpdata
        elif tmpdata==None:#db error ,return
            return None
#   数据格式:{'表名1':searchonetable返回的list1,'表名2':searchonetable返回的list2...}
    return rtdata

#参数:表名,元组/列表类型的列名,搜索内容
def search_one_table(tablename,columnnames,content):
    global db,dbcursor
    #return value:
    #None if db error.
    #[] if no search result.
    #rtdata([]type) if there is data.

    #cmdstr="SELECT * FROM "+tablename+" WHERE tokenize("+" || ' ' || ".join(columnnames)+")@@tokenize('"+content+" "+content.lower()+" "+content.upper()+"');"
    #cmdstr="SELECT * FROM "+tablename+" WHERE to_tsvector('chinesecfg',"+" || ' ' || ".join(columnnames)+")@@to_tsquery('chinesecfg','"+content+"');"

    contentlists=content.split()
    for i in range(len(contentlists)):
        contentlists[i]="("+contentlists[i]+")"
    cnlists=list(columnnames)
    cmdstr="SELECT %s FROM %s where %s ~*'.*(%s).*';"%(','.join(cnlists),tablename," || ' ' || ".join(cnlists),'|'.join(contentlists))
    print cmdstr
    try:
        #执行检索
        dbcursor.execute(cmdstr)
        db.commit()
    except:
        connect()
        db.rollback()
        return None
    rtdata=[]
    rtdata.append(columnnames)
    rtdata.extend(dbcursor.fetchall())
    if len(rtdata)==1:
        return []
    else:
        #数据格式:[(列1名,列2名...),(列1数据,列2数据...),(列1数据,列2数据...)...]
        return rtdata

