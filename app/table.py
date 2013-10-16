# coding=utf-8

import web
import form
from form import DynamicForm,custom_form
import models
from config import render
import re

urls = (
        '/createtable/?','createtable',
         #format : aA0_中--01
        ur'/createcolumns/([a-zA-Z0-9_\u4e00-\u9fa5]+--[1-9][0-9]?)$','createcolumns')

datatype = models.datatype

class createtable:
    def GET(self):
        f = form.table_form()
        return render.createtable(f)

    def POST(self):
        f = form.table_form() 
        if not f.validates():
            return render.createtable(f)
        else:
           raise web.seeother('/createcolumns/' + f.d.tablename + '--' + f.d.columns)

class createcolumns:

    def GET(self,text):
        num = int(text.split('--')[1])
        f = DynamicForm()
        custom_form(f,num)
        print num
        return render.columns(f)

    def POST(self,text):
        num = int(text.split('--')[1])
        tablename = text.split('--')[0]
        f = DynamicForm()
        custom_form(f,num)
        if not f.validates():
            msg = ERR_COL_EDIT
            return render.columns(f,msg)
        else:
            fnames = [models.any2str(f["name" + str(i)].value) for i in range(num)]
            fattrs = [models.any2str(f["attr" + str(i)].value) for i in range(num)]
            attrs = {models.any2str('PK'):models.any2str(f["primarykey"].value)}
            msg = models.create_table(models.any2str(tablename),fnames,fattrs,attrs)
            if msg!='':
                return render.columns(f,msg)
            else:
                raise web.seeother('/../')

app = web.application(urls,locals()) 
