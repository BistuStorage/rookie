#_*_ coding:utf-8 _*_

import web
import sys
from app import table, importdata, search, models
from config import render

urls=(
        '/?','app.search.search',
        '/table',table.app,
        '/importdata',importdata.app
        )


if __name__== "__main__":
    models.connect()
    app=web.application(urls,globals())
    app.run()
