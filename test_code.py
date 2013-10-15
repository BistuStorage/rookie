#coding=utf-8

from paste.fixture import TestApp
from nose.tools import *
import code
from code import app

class TestCode():
    def test_createtable(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        for idx in range(20,20):
            url = '/table/createcolumns/表%d--1' % idx
            res = testApp.get(url)
            form = res.form
            form['name0'] = u'isbn'
            form['attr0'] = u'text'
            form['primarykey'] = u''
            form.submit()
    def test_importdata(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        for idx in range(20):
            url = '/importdata/fromexcel'
            res = testApp.get(url)
            form = res.form
            form['tablename'] = u"table%d" % idx
            form['xlsfile'] = 
            form.submit()
    def test_search(self):
        pass
