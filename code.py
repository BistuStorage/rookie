#_*_ coding:utf-8 _*_

import web
import sys
from app import table,importdata,search
import config
from config import render
from app import models

urls=(
        '/','app.search.search',
        '/table',table.app,
        '/importdata',importdata.app
        )

app=web.application(urls,globals())

if __name__=="__main__":
    models.connect()
    app.run()
