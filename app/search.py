# coding=utf-8

import web
import urllib
import models
import form
from config import render

class search:
    def GET(self):
        f=form.search_form()
        argvdic={}
        argvdic['f']=f
        return render.search(argvdic)

    def POST(self):
        f=form.search_form()
        argvdic={}#传给模板的参数
        argvdic['f']=f
        if not f.validates():
            return render.search(argvdic)
        else:
            rtdata=models.search_all_tables(f.d.content)
            argvdic['rtdata']=rtdata#if no rows returns,then there is not col names
            return render.search(argvdic)
