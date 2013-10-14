# coding=utf-8

from paste.fixture import TestApp
from nose.tools import *
import code
from code import app

class TestCode():
    def test_createtable(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))

        for idx in range(10,20):
            url = '/table/createcolumns/table%d__1' % idx
            res = testApp.post(url,params={'name0':u'isbn','attr0':u'text','primarykey':u''})
#            testApp.submit()
