import web

web.config.debug = True 
web.config.reload = True

web.internalerror=web.debugerror

render = web.template.render('templates/',base='base')
