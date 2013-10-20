# coding=utf-8

import web
import form
from form import DynamicForm,custom_form
import models
import re
from msg import *

urls = (
        '/createtable/?','createtable',
         #format : aA0_中--01
        ur'/createcolumns/([a-zA-Z0-9_\u4e00-\u9fa5]+--[1-9][0-9]?)$','createcolumns')

app = web.application(urls,locals()) 
datatype = models.datatype

#说明： render必须这样写，
#       因为，只能有一个session实例，
#       在主应用中创建，但是子应用不能访问主应用的session，
#       只有通过将session传到web.ctx.session中，这样子应用才能访问session,
#       但是web.ctx是一个线程的字典，
#       也就是说只有在线程中调用，所以不能在任何线程用不到的地方定义，
#       作为每个类里面的类成员也不行，只有return时直接用

class createtable:
    def GET(self):
        if web.ctx.session.login==True:
            f = form.table_form()
            return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).createtable(f)
        else:
            raise web.seeother("/../")

    def POST(self):
        if web.ctx.session.login==True:
            f = form.table_form() 
            if not f.validates():
                return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).createtable(f)
            else:
               raise web.seeother('/createcolumns/' + f.d.tablename + '--' + f.d.columns)
        else:
            raise web.seeother("/../")

class createcolumns:
    def GET(self,text):
        if web.ctx.session.login==True:
            num = int(text.split('--')[1])
            f = DynamicForm()
            custom_form(f,num)
            print num
            return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).columns(f)
        else:
            raise web.seeother("/../")

    def POST(self,text):
        if web.ctx.session.login==True:
            num = int(text.split('--')[1])
            tablename = text.split('--')[0]
            f = DynamicForm()
            custom_form(f,num)
            if not f.validates():
                msg = ERR_COL_EDIT
                return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).columns(f,msg)
            else:
                fnames = [models.any2str(f["name" + str(i)].value) for i in range(num)]
                fattrs = [models.any2str(f["attr" + str(i)].value) for i in range(num)]
                attrs = {models.any2str('PK'):models.any2str(f["primarykey"].value)}
                msg = models.create_table(models.any2str(tablename),fnames,fattrs,attrs)
                if msg!='':
                    return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).columns(f,msg)
                else:
                    raise web.seeother('/../')
        else:
            raise web.seeother("/../")
