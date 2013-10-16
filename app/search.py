# coding=utf-8

import web
import urllib
import models
import form
from config import render

class search:

    def GET(self):
        f = form.search_form()
        return render.search(f)

    def POST(self):
        f = form.search_form()
        if not f.validates():
            return render.search(f)
        else:
            rtdata = models.search_all_tables(models.any2str(f.d.content))
            if rtdata==None:
                return render.search(f,u"数据库处理出错！")
            elif rtdata=={}:
                return render.search(f,u"无结果！")
            else:
                return render.search(f,u"本次查询结果：",rtdata)
