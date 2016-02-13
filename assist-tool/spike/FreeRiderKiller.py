# -*- coding: utf8 -*-
import urllib2
import urllib
import http.cookiejar
import bs4
import time

#Set username and password
username = 'username'
password = 'password'


print '--- Initializing ---'
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

print '--- Geting Cookie ---'
urllib2.urlopen('http://www.baidu.com/')

print '--- Geting Token ---'
token = eval(urllib2.urlopen('https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login').read())['data']['token']
print "Token: " + token

print '--- Sign In Posting ---'
postdata = {
    'token' : token,
    'tpl' : 'pp',
    'username' : username,
    'password' : password,
}
request = urllib2.Request('https://passport.baidu.com/v2/api/?login', urllib.urlencode(postdata))
request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
request.add_header('Accept-Encoding','gzip,deflate,sdch');
request.add_header('Accept-Language','zh-CN,zh;q=0.8');
request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
request.add_header('Content-Type','application/x-www-form-urlencoded');
urllib2.urlopen(request)

print '--- WaterB Checking---'
html = urllib2.urlopen('http://tieba.baidu.com/f?kw=c%D3%EF%D1%D4&fr=index').read();
soup = bs4.BeautifulSoup(html, "html.parser");
n = soup.select('.badge_index')[0].string
print 'WaterB level: ' + n

print '--- Delete Posting ---'
tbs = eval(urllib2.urlopen('http://tieba.baidu.com/dc/common/tbs').read())['tbs']
postdata = {
    'commit_fr' : 'pb',
    'ie' : 'utf-8',
    'tbs' : tbs,
    'kw' : 'c%E8%AF%AD%E8%A8%80',
    'fid' : '22545',
    'tid' : '4261612043',#tie zi id
    'is_vipdel' : '1',
    'pid' : '82142227541',#lou ceng id
    'is_finf' : 'false'
}
request = urllib2.Request('http://tieba.baidu.com/f/commit/post/delete', urllib.urlencode(postdata))
request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
request.add_header('Accept-Encoding','gzip,deflate,sdch');
request.add_header('Accept-Language','zh-CN,zh;q=0.8');
request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
request.add_header('Content-Type','application/x-www-form-urlencoded');
result = urllib2.urlopen(request)
print result.read()

print '--- Done ---'