# -*- coding: utf8 -*-
import cookielib
import gzip
import json
import StringIO
import time
import urllib
import urllib2

# 'generic' tieba request
def genericPost(url, postdata):
    request = urllib2.Request(url, urllib.urlencode(postdata))

    request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
    request.add_header('Accept-Encoding','gzip,deflate,sdch');
    request.add_header('Accept-Language','zh-CN,zh;q=0.8');
    request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
    request.add_header('Content-Type','application/x-www-form-urlencoded');

    data = genericGet(request)

    return data

def genericGet(url):
    connection = urllib2.urlopen(url, timeout = 1)
    data = connection.read()
    connection.close()

    return data


# delete a post with its tid and pid 
def deleteThread(threadData):
    print '--- Deleting ---'

    data = genericGet('http://tieba.baidu.com/dc/common/tbs')
    tbs = json.loads(data)['tbs']

    postdata = {
        'commit_fr' : 'pb',
        'ie' : 'utf-8',
        'tbs' : tbs,
        'kw' : config['name'],
        'fid' : config['fid'],
        'tid' : threadData['tid'], #tie zi id: e.g.'4304106830'
        'is_vipdel' : '0',
        'pid' : threadData['pid'], #lou ceng id: e.g.'82457746974'
        'is_finf' : 'false'
    }
    data = genericPost('http://tieba.baidu.com/f/commit/post/delete', postdata)
    err_code = json.loads(decodeGzip(data))['err_code']

    if err_code == 0:
        print '--- Delete succeessful ---'
        recordHistory(threadData, 'delete')
        return True
    else:
        print '--- Delete failed ---'
        logFile = open('error.log', 'a')
        logFile.write(time.asctime() + '\n')
        logFile.write('Delete failed error code' + err_code + '\n\n')
        logFile.close()
        return False

# block list of user with their username and pid(pid may not be necessary)
def blockID(threadData):
    print '--- Blocking ---'

    constantPid = '82459413573'

    data = genericGet('http://tieba.baidu.com/dc/common/tbs')
    tbs = json.loads(data)['tbs']

    postdata = {
        'day' : '1',
        'fid' : config['fid'],     #??????? 
        'tbs' : tbs,
        'ie' : 'utf-8',
        'user_name[]' : threadData['author'].encode('utf-8'),
        'pids[]' : constantPid, 
        'reason' : '根据帖子标题或内容，判定出现 伸手，作业，课设，作弊，二级考试，广告，无意义水贴，不文明言行或对吧务工作造成干扰等（详见吧规）违反吧规的行为中的至少一种，给予封禁处罚。如有问题请使用贴吧的申诉功能。'
    }
    data = genericPost('http://tieba.baidu.com/pmc/blockid', postdata)
    err_code = json.loads(decodeGzip(data))['err_code']

    if err_code == 0:
        print '--- Block succeessful ---'
        recordHistory(threadData, 'block')
        return True
    else:
        print '--- Block failed ---'
        logFile = open('error.log', 'a')
        logFile.write(time.asctime() + '\n')
        logFile.write('Block failed error code' + err_code + '\n\n')
        logFile.close()
        return False

# tieba admin user login
def adminLogin(username, password):

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    #Geting Cookie
    genericGet('http://www.baidu.com/')

    #Geting Token
    data = genericGet('https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login')
    token = json.loads(data.replace('\'', '"'))['data']['token']

    print '--- Logining ---'
    postdata = {
        'token' : token,
        'tpl' : 'pp',
        'username' : username,
        'password' : password,
    }
    genericPost('https://passport.baidu.com/v2/api/?login', postdata)

    if 'BDUSS' in str(cj):
        print "--- Login succeessful ---"
        return True
    else:
        print "--- Login failed ---"
        return False

def decodeGzip(data):
    fileObj = StringIO.StringIO(data)
    gzipObj = gzip.GzipFile(fileobj = fileObj)
    gzipData = gzipObj.read()
    fileObj.close()
    gzipObj.close()

    return gzipData

def recordHistory(threadData, logType):
    logFile = open('history.log', 'a')

    if logType == 'delete':
        logFile.write('{\n')
        logFile.write('    "type" : "delete",\n')
        logFile.write('    "data" : {\n')
        logFile.write('        "time" : "' + time.asctime() + '",\n')
        logFile.write('        "title" : "' + threadData['title'].encode('utf-8') + '",\n')
        logFile.write('        "author" : "' + threadData['author'].encode('utf-8') + '",\n')
        logFile.write('        "abstract" : "' + threadData['abstract'].encode('utf-8') + '",\n')
        logFile.write('    }\n')
        logFile.write('},\n')
    elif logType == 'block':
        logFile.write('{\n')
        logFile.write('    "type" : "block",\n')
        logFile.write('    "data" : {\n')
        logFile.write('        "time" : "' + time.asctime() + '",\n')
        logFile.write('        "author" : "' + threadData['author'].encode('utf-8') + '",\n')
        logFile.write('    }\n')
        logFile.write('},\n')

    logFile.close()
