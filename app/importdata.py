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
        fef=form.fromexcel_form()
        argvdic={}
        argvdic['fef']=fef
        return render.importdatafromexcel(argvdic)
    
    def POST(self):
        fef=form.fromexcel_form()
        argvdic={}
        argvdic['fef']=fef
        fileinfo=web.input(xlsfile={})
        if not fef.validates():
            argvdic['fef']=form.fromexcel_form()
            argvdic['message']= TABLE_NAME_ERR
            return render.importdatafromexcel(argvdic)
        else:
            filedir= UPLOADDIR
            filepath=fileinfo.xlsfile.filename.replace('\\','/')
            filename=filepath.split('/')[-1]
            fout=open(filedir+'/'+filename,'w')
            fout.write(fileinfo.xlsfile.file.read())
            fout.close()
            rtmessage=models.intodb_xls(fef.d.tablename,filedir+'/'+filename)
            message=""
            if rtmessage['errorcode']==1:
                message=u"此表不存在！"
            elif rtmessage['errorcode']==2:
                message=u"文件不符合要求！"
            elif rtmessage['errorcode']==3:
                message=u"导入表与目标表列数不一致"
            else:
                message=fileinfo.xlsfile.filename+u"成功导入"+fef.d.tablename+u"表！成功插入列数："+str(rtmessage['rightrownums'])+u"失败插入列数："+str(rtmessage['wrongrownums'])
            argvdic['fef']=form.fromexcel_form()#create a new one
            argvdic['message']=message
            return render.importdatafromexcel(argvdic)

app=web.application(urls,locals())
