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
            ret = models.search_all_tables(f.d.content)
            return render.search(f,ret)
