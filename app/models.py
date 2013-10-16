#coding=utf-8

import psycopg2
import xlrd

dbcursor=None
db=None

datatype = ['smallint','integer','bigint','real','numeric','double','serial','bigserial','text','date','time','boolean']
strdatatype=['text']

DB_ERROR=u"数据库操作出错！"

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
def any2str(data):
    if isinstance(data,unicode):
        return data.encode('utf-8')
    else:
        return str(data)
'''
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
'''
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
        print "插入行： %s 失败！"%(",".join(values))
        return DB_ERROR
    return ''
def intodb_xls(tablename,file):
    global db,dbcursor
    
    #get fields
    cmdstr="SELECT fields FROM dbm WHERE name='%s';" % (tablename)
    print cmdstr
    try:
        dbcursor.execute(cmdstr)
        fields=dbcursor.fetchone()
        db.commit()
    except:
        db.rollback()
        return DB_ERROR
    if not fields:
        return u"表不存在！"
    else:
        fields=fields[0].split(",")
        coltyps=[]
        for fs in fields:
            coltyps.append(any2str(fs.split('_')[1]))
    #open file
    try:
        data=xlrd.open_workbook(file)
        table=data.sheets()[0]
    except:
        return u"打开文件错误！"
    #check table
    if table.ncols!=len(coltyps):
        return u"表的列数不符！"
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
    return u"成功导入%s表！成功插入列数：%s 失败插入列数：%s"%(tablename,any2str(nsuc),any2str(nfai))

def if_table_exists(tablename):
    global db,dbcursor

    cmdstr="SELECT name FROM dbm WHERE name='%s' ;"%(tablename)
    print cmdstr
    try:
        dbcursor.execute(cmdstr)
        rt=dbcursor.fetchall()
    except:
        db.rollback()
        return DB_ERROR
    db.commit()
    if rt:
        return u"表已存在！"
    return ''
# fields and attrs are  dicts
def create_table(tablename,fnames,fattrs,attrs):
    global db,dbcursor

    #check tablename
    rt=if_table_exists(tablename)
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
            return u"主键非空时，其值必须是一个或多个列名，多个时用逗号隔开！"
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
        db.rollback()
        return DB_ERROR
    typelists=['text','text']
    values=[tablename]#tablename
    values.append(",".join([fnames[i]+"_"+fattrs[i] for i in range(len(fnames))]))#colname_attr
    rt=insert_column('dbm',tuple(values),tuple(typelists))
    if rt!='':
        db.rollback()#insert into dbm fail
        return rt
    db.commit()#create table and insert into dbm must be one
    return ''
    
def search_all_tables(content):
    global db,dbcursor
    #return value:
    #None if db error.
    #{} if no result.
    #rtdata({}type) if there is data.

    cmdstr="SELECT * FROM DBM;"
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
    return rtdata#数据格式:{'表名1':searchonetable返回的list1,'表名2':searchonetable返回的list2...}

def search_one_table(tablename,columnnames,content):#参数:表名,元组/列表类型的列名,搜索内容
    global db,dbcursor
    #return value:
    #None if db error.
    #[] if no search result.
    #rtdata([]type) if there is data.

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
    print cmdstr
    try:
        dbcursor.execute(cmdstr)#执行检索
        db.commit()
    except:
        db.rollback()
        return None
    rtdata=[]
    rtdata.append(columnnames)
    rtdata.extend(dbcursor.fetchall())
    if len(rtdata)==1:
        return []
    else:
        return rtdata#数据格式:[(列1名,列2名...),(列1数据,列2数据...),(列1数据,列2数据...)...]

