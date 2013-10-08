#_*_ coding: utf-8 _*_
import web
from web import form
import psycopg2
import xlrd

render = web.template.render('templates/')
urls=('/','home',
	'/import/fromexcel','importfromexcel'
	)
db=None
dbcursor=None
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
class home:
	if __name__ == "__main__":
		app=web.application(urls,globals())
		app.run()
	def GET(self):
		importfromexcelurl="/import/fromexcel"
		return render.home(importfromexcelurl)
class importfromexcel:
	def GET(self):
		return render.importfromexcel(None)
	def POST(self):
		x=web.input(xlsfile={})
		filedir='uploadfile'
		if 'xlsfile' in x and x.xlsfile.filename:
			try:
				filepath=x.xlsfile.filename.replace('\\','/')
				filename=filepath.split('/')[-1]
				fout=open(filedir+'/'+filename,'w')
				fout.write(x.xlsfile.file.read())
				fout.close()
				intodb(filedir+'/'+filename)
				return render.importfromexcel(filename+" is imported successfully")
			except:
				return render.importfromexcel("handle error!")
		else:
			return render.importfromexcel("please choose the file.xlsfile is not uploaded")
