from threading import Timer
import queue
import urllib.request
import time
import _thread as thread
from xml.dom.minidom import parse, parseString
import datetime
from db import *


stdoutmutex=thread.allocate_lock()


#Create the data Queue
feedQueue = queue.Queue()
feedQueue.last_published = datetime.datetime(1980,1,1,1,1)
strp_format = '%Y-%m-%dT%H:%M:%SZ'


def putFeed(i):
  time.sleep(1)
  url_request = 'http://api.flickr.com/services/feeds/photos_public.gne'
  url_response = urllib.request.urlopen(url_request)
  response_string = parseString(url_response.read())
  
  entries =  response_string.firstChild.getElementsByTagName('entry')
  first_entry = response_string.firstChild.getElementsByTagName('entry')[0]
  for entry in entries:
     publication_date_string = entry.getElementsByTagName('published')[0].firstChild.toxml()
     publication_date = datetime.datetime.strptime(publication_date_string,strp_format)
     if publication_date > feedQueue.last_published:
  
        feedQueue.put([entry])
  last_published_date_string = first_entry.getElementsByTagName('published')[0].firstChild.toxml()
  last_published_date = datetime.datetime.strptime(last_published_date_string,strp_format)
  feedQueue.last_published = last_published_date
def getFeed(i):
    while feedQueue.empty() == False: 
      entry_data = {}
      entry = feedQueue.get(block=False)[0]
      entry_data['author'] = entry.getElementsByTagName('name')[0].firstChild.toxml().replace("'","")
      entry_data['title'] = entry.getElementsByTagName('title')[0].firstChild.toxml().replace("'","")
      entry_data['buddy_icon'] = entry.getElementsByTagName('flickr:buddyicon')[0].firstChild.toxml().replace("'","")
      entry_data['static_url'] = entry.getElementsByTagName('link')[1].getAttribute('href').replace("'","")
      
      
      insert_string = "INSERT INTO entry (author,title,buddy_icon,static_url) VALUES ('{author}','{title}','{buddy_icon}','{static_url}');".format(**entry_data)
      cur.execute(insert_string)
      print('inserted')
    #except:
    #  #insert_string = "INSERT INTO entry (author,title,buddy_icon,static_href) VALUES ('{author}','(title}','{buddy_icon}','{static_href}');".format(**entry_data)
    #  print('feed fully cached')
    #  break
      conn.commit()



#Create Consumer Thread
#consumer = Timer(3.0,getFeed())

if __name__ == '__main__':
  while True:
    thread.start_new_thread(putFeed,(1,))
    time.sleep(2)
    thread.start_new_thread(putFeed,(1,))
    time.sleep(2)
    thread.start_new_thread(getFeed,(1,))
