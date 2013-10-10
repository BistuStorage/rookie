# coding=utf-8

import web
from web import form
import db

render = web.template.render('templates/')

urls = ('/createtable','createtable',
        '/createcolumns/(.*)','createcolumns')

datatype = ['integer','numeric','text','data','boolean']

table_form = form.Form(
        form.Textbox("tablename",form.notnull,description="tablename"),
        form.Textbox("columns",form.notnull,description="cloumn_numbers"),
        )


class DynamicForm(form.Form):
    def add_input(self, new_input):
        list_inputs = list(self.inputs)
        list_inputs.append(new_input)
        self.inputs = tuple(list_inputs)

class createtable:
    def GET(self):
        f = table_form()
        return render.createtable(f)

    def POST(self):
        f = table_form() 
        if not f.validates():
            return render.createtable(f)
        else:
           raise web.seeother('/createcolumns/' + f.d.tablename + '__' + f.d.columns)

def custom_form(f,num):
    for idx in range(num):
        f.add_input(form.Textbox('name' + str(idx),form.notnull))
        f.add_input(form.Dropdown('attr' + str(idx),datatype))
    f.add_input(form.Textbox("pk"))
    return f

class createcolumns:
    def GET(self,text):
        num = int(text.split('__')[1])
        f = DynamicForm()
        custom_form(f,num)
        return render.columns(f)

    def POST(self,text):
        num = int(text.split('__')[1])
        tablename = text.split('__')[0]
        f = DynamicForm()
        custom_form(f,num)
        if not f.validates():
            return render.columns(f)
        else:
            fnames = [f["name" + str(i)].value for i in range(num)]
            fattrs = [f["attr" + str(i)].value for i in range(num)]
            fields = dict(zip(fnames,fattrs))
            attrs = []
            db.create_table(tablename,fields,attrs)
            return "Successfull!!"

app = web.application(urls,locals()) 
