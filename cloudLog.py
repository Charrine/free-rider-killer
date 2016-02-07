# -*- coding: utf8 -*-
import requests
from datetime import datetime
def postToCloud(threadData, key):
    postdata = {
        'title' : threadData['title'],
        'author' : threadData['author'],
        'abstract' : threadData['abstract'],
        'tid' : threadData['tid'],
        'pid' : threadData['pid'],
        'replyNum' : threadData['replyNum'],
        'operationTime' : threadData['operationTime'],
        # 'operation' : threadData['operation'],
        'grade' : threadData['grade'],
        'keywords' : ','.join(threadData['keywords']),
        'operation' : threadData['operation'],
        'operator' : key,

    }
    r = requests.post("http://yukisora.moe/tieba/post.php", data = postdata)
    if r.content == 'poi':
        return True
    else:
        return False
