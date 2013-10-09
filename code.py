#_*_ coding:utf-8 _*_

import web
import db
import urllib

web.config.debug = True 
web.config.reload = True

importfromexcelurl="/import/fromexcel"
render = web.template.render('templates/')
urls=('/','home',
        '/import/fromexcel','importfromexcel'
        )

db.connect()

def urlform2dic(data):
    datalist=data.split('&')
    datadic={}
    for x in datalist:
        y=x.split('=')
        datadic[urllib.unquote(y[0])]=urllib.unquote(y[1])
    return datadic

class home:
    if __name__ == "__main__":
        app=web.application(urls,globals()) 
        app.run()
    def GET(self):
        return render.home(importfromexcelurl,None)
    def POST(self):
        datadic=urlform2dic(web.data())
        content=datadic['content']
        rtdata=db.search(content)
        return render.home(importfromexcelurl,rtdata)
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
