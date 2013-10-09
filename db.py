import psycopg2
import xlrd

dbcursor=None
db=None
def connect():
	global db,dbcursor
	db=psycopg2.connect(database='mydb',user='postgres',password='allmylove')
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
	for i in range(1,table.nrows):
		cmdstr="insert into book values('"+table.row(i)[0].value+"','"+table.row(i)[1].value+"')"
		dbcursor.execute(cmdstr)
	db.commit()
	disconnect()
