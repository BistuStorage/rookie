# coding=utf-8

import web
import urllib
import models
from config import render

def urlform2dic(data):
    datalist=data.split('&')
    datadic={}
    for x in datalist:
        y=x.split('=')
        datadic[urllib.unquote(y[0])]=urllib.unquote(y[1])
    return datadic

class search:
    def GET(self):
        argvdic={}
        return render.search(argvdic)
    def POST(self):
        datadic=urlform2dic(web.data())
        content=datadic['content']
        argvdic={}#传给模板的参数
        if content:#搜索内容不能为空
            rtdata=models.search(content)
            argvdic['rtdata']=rtdata#结果可以为空
        return render.search(argvdic)

