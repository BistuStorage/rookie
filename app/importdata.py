# coding=utf-8

import web
import form
import models
from config import render, UPLOADDIR
from msg import *

urls=(
    '/?','Import',
)

def importdata(tablename,filetype,datafile):

    filepath = datafile.filename.replace('\\','/')
    filename = filepath.split('/')[-1]
    fout = open(UPLOADDIR+'/'+filename,'w').write(datafile.file.read())
    msg = ""
    if filetype == 'xls':    
        msg = models.intodb_xls(tablename,UPLOADDIR+'/'+filename)
    elif filetype == 'csv':
        msg = models.intodb_csv(tablename,UPLOADDIR+'/'+filename)

    return msg

class Import:
    def GET(self):
        f = form.uploadfile_form()
        return render.Import(f)

    def POST(self):
        f = form.uploadfile_form()
        datafile = web.input(datafile={}).datafile
        msg = ''
        if not f.validates():
            msg = ERR_TABLE_NAME
            return render.Import(f,msg)
        else:
            msg = importdata(f.d.tablename,f.d.filetype,datafile)
            return render.Import(f,msg)

app=web.application(urls,locals())
