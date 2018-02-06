# -*- coding: utf-8 -*-
import csv
import requests
import os
import time
import datetime



#print ('loading boards list .....')
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

    #print ('######################### scanning 4chan......')
    #print (rules_list)
    for board in boards:
        #print ('###############################     ' + board)
        total_grabs = 2
        wanted_grabs = 3
        while total_grabs <= wanted_grabs:
            url = ("http://boards.4chan.org/{}/{}".format(board, total_grabs))
            #print ('scanning {}'.format(board))
            #url = ('http://boards.4chan.org/pol/%s' % total_grabs)
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            response = requests.get(url, headers=headers)
            stuff = response.text.split('<br>')
            for post in stuff:
                i = post.split('a href="thread/')
                if '"replylink">Reply<' in str(i):
                    i = str(i).split('[')
                    #i = i.split(']')
                    sub = i[2].split('" class=')[0]
                    if "<', '" in sub:
                        sub = sub.replace("<', '", "")
                        #print (board+'/thread/'+sub)
                        #print ('#############################')
                        if sub not in subT:
                            subT.append(board+'/thread/'+sub)
                        #print (i[2])
            total_grabs += 1

def fill_x():
    #print ('######################### matching against list......')
    #print (rules_list)
    for sub in subT:
        #print (sub)
        url = ("http://boards.4chan.org/{}".format(sub))
        #print ('scanning {}'.format(board))
        #url = ('http://boards.4chan.org/pol/%s' % total_grabs)
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
                                    #print (line)
                                    x.append(line)


scan_chan()
fill_x()
print (x)
