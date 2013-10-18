import web

web.config.debug = True
web.config.reload = False
web.internalerror=web.debugerror

import os
UPLOADDIR = '/'.join(os.path.realpath(__file__).split('/')[:-1]) + "/uploadfile"

db = 'mydb'
user = 'jwzh'
DBM = 'DBM'
MDM = 'MDM'

