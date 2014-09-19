#admin handling
import webapp2
import datetime
import random
from google.appengine.ext import ndb
from google.appengine.api import users
import hashlib
import logging

import json
from Kinds import QuestionKind 



class uploadtable(webapp2.RequestHandler):
    def admin_updatequestiontable(self):
        jsonstring = self.request.body
        jsonobject = json.JSONDecoder().decode(jsonstring);
        questions = jsonobject['question'];
        hints = jsonobject['hints']
        words = jsonobject['words']
        response = [];
        #tobe added as a job . lets see.
        for question,hintlist,wordlist in zip(questions,hints,words):
            qid = int(hashlib.sha1(question).hexdigest(), 16) % (10 ** 8);
            randomnumber = random.random();
            hintlist = hintlist.split(':');
            wordlist = wordlist.split(':');
            q = QuestionKind(parent = ndb.Key(QuestionKind,qid),question=question,hints=hintlist,wordlist = wordlist,randomID=randomnumber,qid=qid)
            q.put();
            response.append(str(qid));
            logging.debug('successful upda')
            
        return 'admin update successful : key Gen :: '+','.join(response);
            
        
        #dictionary = self.request.POST['EQ']
        question = self.request.POST['question'];
        hints = self.request.POST['hints'];
        words = self.request.POST['words'];
        
        
        
        #question only in hash since hints can be updated later too, if dict gets updated :)
        
        

    def post(self):
        response_string = 'INVALID ACCESS';        
        
        #Check authorization
        

        response_string = self.admin_updatequestiontable();                
        self.response.write(response_string);
        
    
app = webapp2.WSGIApplication([('/uploadtable', uploadtable)],
                              debug=True)
