# coding=utf-8

import web
import form
import models
from config import  UPLOADDIR
from msg import *

urls=(
    '/?','Import',
)

app=web.application(urls,locals())

#说明： render必须这样写，
#       因为，只能有一个session实例，
#       在主应用中创建，但是子应用不能访问主应用的session，
#       只有通过将session传到web.ctx.session中，这样子应用才能访问session,
#       但是web.ctx是一个线程的字典，
#       也就是说只有在线程中调用，所以不能在任何线程用不到的地方定义，
#       作为每个类里面的类成员也不行，只有return时直接用

def importdata(tablename,filetype,datafile,sep):
    filepath = datafile.filename.replace('\\','/')
    filename = filepath.split('/')[-1]
    try:
        fout = open(UPLOADDIR+'/'+filename,'w')
        fout.write(datafile.file.read())
        fout.close()
    except:
        return ERR_FILE_OPEN
    msg = ""
    if filetype == 'xls':    
        msg = models.intodb_xls(tablename,UPLOADDIR+'/'+filename)
    elif filetype == 'csv':
        msg = models.intodb_csv(tablename,UPLOADDIR+'/'+filename,sep)
    return msg

class Import:
    def GET(self):
        if web.ctx.session.login==True:
            f = form.uploadfile_form()
            return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).Import(f)
        else:
            raise web.seeother("/../")
            
    def POST(self):
        if web.ctx.session.login==True:
            f = form.uploadfile_form()
            datafile = web.input(datafile={}).datafile
            msg = ''
            if not f.validates():
                msg = ERR_TABLE_NAME
                return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).Import(form.uploadfile_form(),msg)#这儿必须返回新的form，不然会出错
            else:
                msg = importdata(models.any2str(f.d.tablename),models.any2str(f.d.filetype),datafile,models.any2str(f.d.sep))
                return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).Import(form.uploadfile_form(),msg)#这儿也一样
        else:
            raise web.seeother("/../")
