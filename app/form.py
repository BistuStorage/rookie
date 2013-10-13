# coding=utf-8

from web import form
from models import datatype

table_form = form.Form(
        form.Textbox("tablename",form.notnull,description=u"表名"),
        form.Textbox("columns",form.notnull,description=u"列数"),
        )

fromexcel_form = form.Form(
    form.Textbox("tablename",form.notnull,description=u"表名"),
    form.File("xlsfile",form.notnull,description=u"文件"),
    )

search_form=form.Form(
    form.Textbox("content",form.notnull),
    )

class DynamicForm(form.Form):
    def add_input(self, new_input):
        list_inputs = list(self.inputs)
        list_inputs.append(new_input)
        self.inputs = tuple(list_inputs)

def custom_form(f,num):
    for idx in range(num):
        f.add_input(form.Textbox('name' + str(idx),form.notnull))
        f.add_input(form.Dropdown('attr' + str(idx),datatype))
    f.add_input(form.Textbox("primarykey"))
    return f
