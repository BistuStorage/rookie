#!/usr/bin/env python2
# coding=utf-8

import httplib
import json

fw = open('csvfile/book2.csv','w')

def any2str(data):
    if isinstance(data,unicode):
        return data.encode('utf-8')
    else:
        return str(data)

def insert(info):
    flist = [info['title'],info['year'],info['directors'][0]['name'],info['countries'][0],info['rating']['average']]
    flist = [any2str(f) for f in flist]
    print info['title'],type(info['title'])
    fw.write(','.join(flist) + '\n')

def get_movie(idx):
    conn.request('GET','/v2/movie/subject/'+idx)
    s = (conn.getresponse().read().decode('utf-8'))
    loc = json.loads(s)
    return loc

conn = httplib.HTTPConnection('api.douban.com')
conn.request('GET','/v2/movie/top250')
s = (conn.getresponse().read().decode('utf-8'))
loc = json.loads(s)
for i in xrange(5,10):
    info = loc["subjects"][i]
    print info["title"],info["id"]
    insert(get_movie(info['id']))
fw.close() 
