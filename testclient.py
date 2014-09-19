#client to update question table
import urllib2
import urllib
import json

command = 'updatequestiontable'
questions = ['1,2,3,4,5,6,7,8,9,10,14,15']
hints = ['','']
url = 'http://www.utopian-genius-615.appspot.com/SliderPage'
#url = 'http://localhost:8080/'
data = json.JSONEncoder().encode({'command' :command,'question':questions,'hints':hints,'words':words});
auth_req = urllib2.Request(url+'uploadtable?',data,{'Content-Type': 'application/json'});
#auth_req = urllib2.Request(auth_uri, data=authreq_data)
auth_resp = urllib2.urlopen(auth_req)
print auth_resp.read();
auth_resp.close()
