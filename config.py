import web

web.config.debug = True
web.config.reload = False
web.internalerror=web.debugerror

#import os
#UPLOADDIR = os.path.realpath(__file__) + "/uploadfile"
UPLOADDIR = "uploadfile"

db = 'mydb'
user = 'postgres'

