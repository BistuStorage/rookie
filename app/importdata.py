# coding=utf-8

import web
import form
import models
from config import render

urls=(
        '/fromexcel','fromexcel'
    )
fromexcel_form = form.fromexcel_form

class fromexcel:
    def GET(self):
        fef=fromexcel_form()
        return render.importfromexcel(fef,None)
    
    def POST(self):
        fef=fromexcel_form()
        if not fef.validates():
            return render.importfromexcel(fef,None)
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
            else:
                message=fileinfo.xlsfile.filename+u"成功导入"+fef.d.tablename+u"表！"
            return render.importfromexcel(fromexcel_form(),message)

app=web.application(urls,locals())
