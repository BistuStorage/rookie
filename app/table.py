# coding=utf-8

import web
import form
from form import DynamicForm,custom_form
import models
from config import render

urls = (
        '/createtable/?','createtable',
        '/createcolumns/(.*)','createcolumns'
        )

datatype = models.datatype

class createtable:
    def GET(self):
        f = form.table_form()
        argvdic={}
        argvdic['f']=f
        return render.createtable(argvdic)

    def POST(self):
        f = form.table_form() 
        if not f.validates():
            argvdic={}
            argvdic['f']=f
            return render.createtable(argvdic)
        else:
           raise web.seeother('/createcolumns/' + f.d.tablename + '__' + f.d.columns)


class createcolumns:
    def GET(self,text):
        num = int(text.split('__')[1])
        f = DynamicForm()
        form.custom_form(f,num)
        argvdic={}
        argvdic['f']=f
        return render.columns(argvdic)

    def POST(self,text):
        num = int(text.split('__')[1])
        tablename = text.split('__')[0]
        f = DynamicForm()
        custom_form(f,num)
        if not f.validates():
            argvdic={}
            argvdic['f']=f
            return render.columns(argvdic)
        else:
            fnames = [f["name" + str(i)].value for i in range(num)]
            fattrs = [f["attr" + str(i)].value for i in range(num)]
            fields = dict(zip(fnames,fattrs))
            attrs = []
            models.create_table(tablename,fields,attrs)
            return "建表成功！"

app = web.application(urls,locals()) 
