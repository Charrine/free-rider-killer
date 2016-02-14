# -*- coding: utf8 -*-
import requests

from datetime import datetime

def postToCloud(threadData, key):
    postdata = {
        'title' : threadData['thread']['title'],
        'author' : threadData['author']['userName'],
        'abstract' : threadData['thread']['abstract'],
        'tid' : threadData['thread']['tid'],
        'pid' : threadData['thread']['pid'],
        'replyNum' : threadData['thread']['replyNum'],
        'operationTime' : threadData['operation']['operationTime'],
        'grade' : threadData['thread']['grade'],
        'keywords' : ','.join(threadData['thread']['keywords']),
        'operation' : threadData['operation']['operation'],
        'operator' : key,

    }
    r = requests.post("http://yukisora.moe/tieba/post.php", data = postdata)
    if r.content == 'poi':
        return True
    else:
        return False
