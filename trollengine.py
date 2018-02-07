# -*- coding: utf-8 -*-
import csv
import requests
import os
import time
import datetime



with open('boards.csv', 'r') as b:
    reader = csv.reader(b)
    boards = list(reader)
    boards = str(boards)
boards = boards.replace('[', '')
boards = boards.replace(']', '')
boards = boards.replace("'","")
boards = boards.split(', ')


x = []
trash = x
subT = []

total_grabs = 2
wanted_grabs = 10


tick = 0
fail_out = 0
cycle = 0



def scan_chan():
    for board in boards:
        url = ("http://boards.4chan.org/{}".format(board))
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        stuff = response.text.split('<br>')
        for post in stuff:
            i = post.split('a href="thread/')
            if '"replylink">Reply<' in str(i):
                i = str(i).split('[')
                sub = i[2].split('" class=')[0]
                if "<', '" in sub:
                    sub = sub.replace("<', '", "")
                    if sub not in subT:
                        subT.append(board+'/thread/'+sub)

def fill_x():
    for sub in subT:
        url = ("http://boards.4chan.org/{}".format(sub))
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        stuff = response.text.split('<br>')
        for i in stuff:
            i = i.split('postMessage')
            for d in i:
                d = d.split('" id="')
                for c in d:
                    c = c.split('quote')
                    for f in c:
                        if '</block' in f:
                            f = f.replace('&#039;',"'")
                            f = f.replace('</a>', '')
                            f = f.replace('</block','')
                            f = f.replace('</span>', '')
                            f = f.replace('">&gt;', '')
                            f = f.replace('&quot;', '"')
                            f = f.split('">')[-1]
                            words = f.split(' ')
                            line = f.replace('\n','')
                            line = line.replace('link&gt;', '')
                            line = line.replace('<b></b></td></tr></table>','')
                            if line:
                                if line.isdigit() == False:
                                    x.append(str(datetime.datetime.now()) +'||'+line+'||'+url)


scan_chan()
fill_x()
print (x)
