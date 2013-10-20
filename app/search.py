# coding=utf-8

import web
import urllib
import models
import form
from msg import *

#说明： render必须这样写，
#       因为，只能有一个session实例，
#       在主应用中创建，但是子应用不能访问主应用的session，
#       只有通过将session传到web.ctx.session中，这样子应用才能访问session,
#       但是web.ctx是一个线程的字典，
#       也就是说只有在线程中调用，所以不能在任何线程用不到的地方定义，
#       作为每个类里面的类成员也不行，只有return时直接用

class search:

    def GET(self):
        print web.ctx.session
        if web.ctx.session.login==True:
            f = form.search_form()
            return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).search(f)
        else:
            raise web.seeother('/session/login')
    def POST(self):
        if web.ctx.session.login==True:
            f = form.search_form()
            alldata=web.input()
            if not f.validates():
                return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).search(f)
            else:
                if alldata.has_key('ismaster'):
                    rtdata=models.search_master(models.any2str(f.d.content))
                else:
                    rtdata = models.search_all_tables(models.any2str(f.d.content))
                if rtdata==None:
                    return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).search(f,ERR_DB)
                elif rtdata=={}:
                    return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).search(f,NO_RESULT)
                else:
                    return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).search(f,THIS_RESULT,rtdata)
        else:
            raise web.seeother('/session/login')
