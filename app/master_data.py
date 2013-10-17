# coding=utf-8

import web
import form
from form import DynamicForm,custom_master
import models
from models import any2str
import config
from config import render

urls = (
        '/table','Table',
        ur'/table/([a-zA-Z0-9_\u4e00-\u9fa5]+)$','Masterdata'
        )

class Table:
    def GET(self):
        f = form.search_form()
        return render.search(f)
    def POST(self):
        f = form.search_form()
        if not f.validates():
            return render.search(f)
        else:
            raise web.seeother('/table/' + f.d.content)
class Masterdata:
    def GET(self,text):
        flist = models.get_field_name(text)
        f = DynamicForm()
        custom_master(f,flist)
        return render.master_data(f)

    def POST(self,text):
        flist = models.get_field_name()
        f = DynamicForm()
        custom_master(f,flist)
        if not f.validates():
            msg = ERR_NOTNULL
            return render.master_data(f,msg)
        else :
            tbinfo = [any2str(text)]
            tbinfo.append(','.join(fn for fn in flist if f[fn].checked)) 
            msg = models.insert_column(config.MDM,tbinfo,('text','text'))
            if msg != '':
                return render.master_data(f,msg)
            else :
                raise web.seeother('/../')

app=web.application(urls,locals())
