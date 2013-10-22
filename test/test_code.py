#coding=utf-8

from paste.fixture import TestApp
from nose.tools import *
import code
from code import app

class TestCode():
    def test_createtable(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        for idx in range(20):
            url = '/table/createcolumns/表%d--1' % idx
            res = testApp.get(url)
            form = res.form
            form['name0'] = u'isbn'
            form['attr0'] = u'text'
            form['primarykey'] = u''
            form.submit()
            print 'xxx'
    def test_importdata(self):
        pass
#j        middleware = []
#j        testApp = TestApp(app.wsgifunc(*middleware))
#j        for idx in range(20):
#j            url = '/importdata/fromexcel'
#j            res = testApp.get(url)
#j            form = res.form
#j            form['tablename'] = u"table%d" % idx
#j            form['xlsfile'] = 
#j            form.submit()
    def test_search(self):
        pass
