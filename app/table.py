# coding=utf-8

import web
import form
from form import DynamicForm,custom_form
import models
from config import render
import re

urls = (
        '/createtable/?','createtable',
        ur'/createcolumns/([a-zA-Z0-9_\u4e00-\u9fa5]+--[1-9][0-9]?)$','createcolumns'#格式：中文、英文、数字、下划线--1到99
        )

datatype = models.datatype

class base(object):
    def __init__(self):
        web.header('Content-type','text/html')

class createtable(base):
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
           raise web.seeother('/createcolumns/' + f.d.tablename + '--' + f.d.columns)

class createcolumns(base):
    def GET(self,text):
        num = int(text.split('--')[1])
        f = DynamicForm()
        form.custom_form(f,num)
        argvdic={}
        argvdic['f']=f
        return render.columns(argvdic)
        #else:
        #    return "tablename is not supported."

    def POST(self,text):
        num = int(text.split('--')[1])
        tablename = text.split('--')[0]
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
            attrs = {'PK':f["primarykey"].value.encode('utf-8')}
            models.create_table(tablename,fields,attrs)
            raise web.seeother('/../')
app = web.application(urls,locals())
