# coding=utf-8

import web
import form
import models
from config import render

urls=(
        '/?','importdata',
        '/fromexcel','fromexcel'
    )
TABLE_NAME_ERR = u"表名格式：中文、英文、数字、下划线，文件非空！"
UPLOADDIR = "uploadfile"
SUC_UP_MSG = u"%s 成功导入 %s 表! 成功插入列数：%s 失败插入列数：%s"

class importdata:
    def GET(self):
        return render.importdata()

class fromexcel:
    def GET(self):
        form = form.uploadfile_form()}
        return render.uploadfile(form,msg)
    
    def POST(self):
        form = form.uploadfile_form()
        xlsfile = web.input(xlsfile={}).xlsfile
        if not form.validates():
            msg = TABLE_NAME_ERR
            return render.uploadfile(form,msg)
        else:
            filedir = UPLOADDIR
            filepath = xlsfile.filename.replace('\\','/')
            filename = filepath.split('/')[-1]
            fout = open(filedir+'/'+filename,'w').write(xlsfile.file.read())
            fout.close()

            rtmsg = models.intodb_xls(fef.d.tablename,filedir+'/'+filename)
            msg = rtmsg['errc']
            if msg = '':
                msg = SUC_UP_MSG %  (xlsfile.filename,form.d.tablename,rtmsg['nsuc'],rtmsg['nfai'])
            return render.uploadfile(form,msg)

app=web.application(urls,locals())
