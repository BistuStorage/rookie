#_*_ coding: utf-8 _*_
#coding=utf-8

import web
from web import form
import db

web.config.debug = True 
web.config.reload = True

render = web.template.render('templates/')
urls=('/','home',
        '/import/fromexcel','importfromexcel'
        )

class home:
    if __name__ == "__main__":
        app=web.application(urls,globals()) 
        app.run()
    def GET(self):
        importfromexcelurl="/import/fromexcel"
        return render.home(importfromexcelurl)

class importfromexcel:
    def GET(self):
        return render.importfromexcel(None)
    def POST(self):
        x=web.input(xlsfile={})
        filedir='uploadfile'
        if 'xlsfile' in x and x.xlsfile.filename:
            try:
                filepath=x.xlsfile.filename.replace('\\','/')
                filename=filepath.split('/')[-1]
                fout=open(filedir+'/'+filename,'w')
                fout.write(x.xlsfile.file.read())
                fout.close()
                db.intodb(filedir+'/'+filename)
                print "OK"
                return render.importfromexcel(filename+" is imported successfully")
            except:
                return render.importfromexcel("handle error!")
        else:
            return render.importfromexcel("please choose the file.xlsfile is not uploaded")
