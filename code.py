#_*_ coding: utf-8 _*_

import web
from web import form
import db

web.config.debug = True 
web.config.reload = True

render = web.template.render('templates/')

urls=(  '/','home',
        '/import/fromexcel','importfromexcel',
        '/custom','createtable'
        )

table_form = form.Form(
        form.Textbox("tablename",description="tablename"),
        form.Textbox("fieldnames",description="fieldnames"),
        form.Textbox("fieldattrs",description="fieldattrs"),
        form.Button("submit",type="submit",description="add"),
        validators = [
                form.Validator("Passwords did't match", lambda i: i.tablename != '')]
        )

class home:
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
                return render.importfromexcel(filename+" is imported successfully")
            except:
                return render.importfromexcel("handle error!")
        else:
            return render.importfromexcel("please choose the file.xlsfile is not uploaded")

class createtable:

    def GET(self):
        f = table_form()
        return render.createtable(f)

    def POST(self):
        f = table_form() 
        if not f.validates():
            return render.createtable(f)
        else:
            fields = dict(zip(f['fieldnames'].value.split(','),f['fieldattrs'].value.split(',')))
            print fields
            db.create_table(f['tablename'].value,fields)

            raise web.seeother('/')

if __name__ == "__main__":

    app=web.application(urls,globals()) 
    db.connect()
    app.run()
