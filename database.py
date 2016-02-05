# -*- coding: utf8 -*-
import requests

def storeIntoDatabase(threadData):
    postdata = {
        'title' : threadData['title'],
        'author' : threadData['author'],
        'abstract' : threadData['abstract'],
        'tid' : threadData['tid'],
        'pid' : threadData['pid'],
        'mark' : '0'
    }
    r = requests.post("http://yukisora.moe/tieba/post.php", data = postdata)
    print r.content

#threadData = {
#    'title' : 'NicoNiconi',
#    'author' : 'Poi',
#    'abstract' : 'NicoNicoNi, NicoNicoNi.',
#    'tid' : '4304106830',
#    'pid' : '82457746974',
#    'mark' : '0'
#}
#storeIntoDatabase(threadData)
