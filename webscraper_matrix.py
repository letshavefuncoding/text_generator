#A webscraper for bbs style websites archival data
#information is gathered and transformed into a matrix to feed into a neural network.
import re
import os
import os.path
import time
import string
import requests
from bs4 import BeautifulSoup
from os import walk


now = time.strftime("%Y%m%d")
#set time to save finished file to the flist_date.txt
hclass="postMessage"
doLink="{domain url}"
aLink='{archive url}'
presponse= requests.get(aLink, timeout=5)
pcontent=BeautifulSoup(presponse.content,"html.parser")
#web variables
linklist=[]
postlist=[]
matList=[]
#all lists: Link, Posts, and matrix
count=0
regex=">>[0-9]+"

#here we aquire all the links to archival data

for text in pcontent.find_all("a", href=True):
       if "thread" in str(text).split("/"):
         linklist.append(text['href'])

"""here we concatinate the domain url with the links gathered 
from the archive, to access all text within the archived links"""

for line in linklist:
    try:
        plink=doLink+line
        presponse= requests.get(plink, timeout=5)
        pcontent=BeautifulSoup(presponse.content,"html.parser")
        for item in pcontent.find_all(class_=hclass):
            if re.match(regex,item.text,flags=0):
                x=re.sub(regex,"",item.text)
                postlist.append(x)

            else:
                postlist.append(item.text)
            count+=1
            if(count%100==0):
                print("item added: "+str(count))

    except:
            print("unable to obtain: "+ plink)


#normalizing and splitting postlist to transform into a matrix
postlist=[word.lower() for word in postlist]
postlist=[word.split() for word in postlist]



#here is where the gathered text information is transformed into a maxtrix to feed the neural network model.
length = 50 + 1

for word in postlist:
    for x in range(length, len(word)):
	  #select sequence of tokens
        seq = word[x-length:x]

	  #convert into a line
        line = ' '.join(seq)
	  #store
        matList.append(line)

f=open("{prefered location}"+now+".txt","w",encoding="utf-8")
data = '\n'.join(matList)
f.write(data)
f.close()