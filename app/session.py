# coding=utf-8
import web
import form
import models
from msg import *

urls=(
    '/login/?','login',
    '/logout/?','logout'
    )
app=web.application(urls,locals())

#说明： render必须这样写，
#       因为，只能有一个session实例，
#       在主应用中创建，但是子应用不能访问主应用的session，
#       只有通过将session传到web.ctx.session中，这样子应用才能访问session,
#       但是web.ctx是一个线程的字典，
#       也就是说只有在线程中调用，所以不能在任何线程用不到的地方定义，
#       作为每个类里面的类成员也不行，只有return时直接用

class login:

    def GET(self):
        if web.ctx.session.login==True:
            raise web.seeother("/../")
        else:
            f=form.login_form()
            return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).login(f)

    def POST(self):
        if web.ctx.session.login==False:
            f=form.login_form()
            if not f.validates():
                msg=ERR_LOGIN_INFO
                return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).login(f,msg)
            else:
                info=web.input()
                msg,pri=models.check_login(info.username,info.password)
                if msg!='':
                    return web.template.render('templates/',base='base',globals={'session':web.ctx.session}).login(f,msg)
                else:
                    web.ctx.session.login=True
                    web.ctx.session.username=info.username
                    web.ctx.session.privilege=pri
                    raise web.seeother("/../")
        else:
            raise web.seeother("/../")
class logout:
    def GET(self):
        if web.ctx.session.login==True:
            web.ctx.session.kill()
        raise web.seeother("/../")
