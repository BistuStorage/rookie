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
           raise web.seeother('/createcolumns/' + f.d.tablename + '--' + f.d.columns)


class createcolumns:
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
        argvdic={}
        argvdic['f']=f
        if not f.validates():
            return render.columns(argvdic)
        else:
            fnames = [unicode(f["name" + str(i)].value) for i in range(num)]
            fattrs = [unicode(f["attr" + str(i)].value) for i in range(num)]
            attrs = {'PK':unicode(f["primarykey"].value)}
            rt=models.create_table(tablename,fnames,fattrs,attrs)
            if rt==1:
                argvdic['message']=u"数据库处理错误！"
                return render.columns(argvdic)
            elif rt==2:
                argvdic['message']=u"表"+tablename+u"已经存在！"
                return render.columns(argvdic)
            elif rt==3:
                argvdic['message']=u"主键必须是一个或多个列名，多个时用逗号分开！"
                return render.columns(argvdic)
            else:
                raise web.seeother('/../')

app = web.application(urls,locals()) 
