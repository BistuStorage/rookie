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

class importdata:
    def GET(self):
        return render.importdata()

class fromexcel:
    def GET(self):
        f = form.uploadfile_form()
        return render.uploadfile(f)
    
    def POST(self):
        f = form.uploadfile_form()
        xlsfile = web.input(xlsfile={}).xlsfile
        if not f.validates():
            msg = TABLE_NAME_ERR
            return render.uploadfile(form.uploadfile_form(),msg)
        else:
            filedir = UPLOADDIR
            filepath = xlsfile.filename.replace('\\','/')
            filename = filepath.split('/')[-1]
            fout = open(filedir+'/'+filename,'w')
            fout.write(xlsfile.file.read())
            fout.close()

            msg = models.intodb_xls(models.any2str(f.d.tablename),models.any2str(filedir+'/'+filename))
            return render.uploadfile(form.uploadfile_form(),msg)

app=web.application(urls,locals())
