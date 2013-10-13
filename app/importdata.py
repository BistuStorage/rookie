# coding=utf-8

import web
import form
import models
from config import render

urls=(
        '/?','importdata',
        '/fromexcel','fromexcel'
    )
class importdata:
    def GET(self):
        return render.importdata()
class fromexcel:
    def GET(self):
        fef=form.fromexcel_form()
        argvdic={}
        argvdic['fef']=fef
        return render.importdatafromexcel(argvdic)
    
    def POST(self):
        fef=form.fromexcel_form()
        argvdic={}
        argvdic['fef']=fef
        if not fef.validates():
            return render.importdatafromexcel(argvdic)
        else:
            filedir="uploadfile"
            fileinfo=web.input(xlsfile={})
            filepath=fileinfo.xlsfile.filename.replace('\\','/')
            filename=filepath.split('/')[-1]
            fout=open(filedir+'/'+filename,'w')
            fout.write(fileinfo.xlsfile.file.read())
            fout.close()
            rt=models.intodb_xls(fef.d.tablename,filedir+'/'+filename)
            message=""
            if rt==1:
                message=u"此表不存在！"
            elif rt==2:
                message=u"文件不符合要求！"
            elif rt==3:
                message=u"导入表与目标表列数不一致"
            else:
                message=fileinfo.xlsfile.filename+u"成功导入"+fef.d.tablename+u"表！"
            argvdic['fef']=form.fromexcel_form()#create a new one
            argvdic['message']=message
            return render.importdatafromexcel(argvdic)

app=web.application(urls,locals())
