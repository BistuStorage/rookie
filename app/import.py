# coding=utf-8

import web
import form
import models
from config import render

urls=(
    '/?','Import',
)
TABLE_NAME_ERR = u"表名格式：中文、英文、数字、下划线，文件非空！"
UPLOADDIR = "uploadfile"
SUC_UP_MSG = u"%s 成功导入 %s 表! 成功插入列数：%s 失败插入列数：%s"

def importdata(tablename,filetype,datafile):

    filepath = datafile.filename.replace('\\','/')
    filename = filepath.split('/')[-1]
    fout = open(UPLOADDIR+'/'+filename,'w').write(datafile.file.read())
    fout.close()

    rtmsg = ""
    if filetype == 'xls':    
        rtmsg = models.intodb_xls(tablename,UPLOADDIR+'/'+filename)
    elif filetype == 'cvs':
        rtmsg = models.intodb_cvs(tablename,UPLOADDIR+'/'+filename)

    msg = rtmsg['errc']
    if msg = '':
        msg = SUC_UP_MSG %  (datafile.filename,tablename,rtmsg['nsuc'],rtmsg['nfai'])

class Import:
    def GET(self):
        form = form.uploadfile_form()}
        return render.Import(form,msg)

    def POST(self):
        form = form.uploadfile_form()
        datafile = web.input(datafile={}).datafile
        if not form.validates():
            msg = TABLE_NAME_ERR
            return render.uploadfile(form,msg)
        else:
            msg = importdata(form.d.tablename,form.d.filetype,datafile)
            return render.uploadfile(form,msg)

app=web.application(urls,locals())
