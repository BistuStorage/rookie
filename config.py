import web

web.config.debug = True 
web.config.reload = True
web.internalerror=web.debugerror

render = web.template.render('templates/',base='base')

#import os
#UPLOADDIR = os.path.realpath(__file__) + "/uploadfile"
UPLOADDIR = "/home/jwzh/Github/rookie/uploadfile"

db = 'mydb'
user = 'jwzh'

