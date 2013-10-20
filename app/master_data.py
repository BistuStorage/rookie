# coding=utf-8

import web
import form
from form import DynamicForm,custom_master
import models
from models import any2str
import config

urls = (
        '/table','Table',
        ur'/table/([a-zA-Z0-9_\u4e00-\u9fa5]+)$','Masterdata'
        )

class Table:
    def GET(self):
        f = form.search_form()
        return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).search(f)
    def POST(self):
        f = form.search_form()
        if not f.validates():
            return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).search(f)
        else:
            raise web.seeother('/table/' + f.d.content)

class Masterdata:
    def GET(self,text):
        text = any2str(text)
        flist,msg = models.get_fields_name(text)
        f = DynamicForm()
        custom_master(f,flist)
        if msg == '' : 
            msg = models.if_table_exists(text,config.MDM)
        return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).master_data(f,msg)

    def POST(self,text):
        text = any2str(text)
        flist,msg = models.get_fields_name(text)
        f = DynamicForm()
        custom_master(f,flist)
        if not f.validates() or msg != '':
            msg = ERR_NOTNULL
            return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).master_data(f,msg)
        else :
            tbinfo = [text]
            fw = web.input()
            mflist = [any2str(flist[idx]) for idx in range(len(flist)) if fw.has_key(str(idx))]
            tbinfo.append(','.join(mflist))
            print tbinfo[1]
            msg = models.insert_column(config.MDM,tbinfo,('text','text'))
            models.db.commit()
            if msg != '':
                return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).master_data(f,msg)
            else :
                raise web.seeother('/../')

app=web.application(urls,locals())
