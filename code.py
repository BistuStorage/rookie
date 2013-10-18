#_*_ coding:utf-8 _*_

import web
import sys
from app import table, importdata, search, models,session

urls=(
        '/?','app.search.search',
        '/session',session.app,
        '/table',table.app,
        '/importdata',importdata.app,
        )
app=web.application(urls,globals())
session=web.session.Session(app,web.session.DiskStore('sessions'),initializer={'login':False,'username':'','privilege':0})
def session_hook():
    web.ctx.session=session
app.add_processor(web.loadhook(session_hook))

if __name__== "__main__":
    models.connect()
    app.run()
