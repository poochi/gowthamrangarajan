# This is a server implementation for slider puzzle
#login not required to request question
#login required to submit scores
#All puzzles
import webapp2
import datetime
import random
from google.appengine.ext import ndb
from google.appengine.api import users
import hashlib
import logging
from Kinds import QuestionKind
from Kinds import QuestionLeaderBoardKind
from Kinds import ContestDetailsKind

import json


class SliderPage(webapp2.RequestHandler):            
    

    def pick_random_question(self):
    	#question type for Lloyd's puzzle .... listof permutation of numbers
        
        attempt = 0;
        questionEntities = []
        while(len(questionEntities)== 0 and attempt <10):
            questionEntities = QuestionKind.query().filter(QuestionKind.randomID >= random.random()).fetch(1);
            
            attempt+=1;
        if attempt == 10:
            return None ;
        print questionEntities
        return [questionEntities[0].qid,questionEntities[0].question,questionEntities[0].hints];
        
    def register_participant(self):
    	#REGISTER based on gmail username

        [qid,ques,hints]= self.pick_random_question();
        if qid == None:

            response_json = json.JSONEncoder().encode({'status':'fail','reason':'Random QpickFailed'})
        else:
            response_json = json.JSONEncoder().encode({'status':'success','reason':'Retrieved a Question',	
            	'question':ques,'hints':hints,'questionid':qid})
        
        
    
        return response_json;

        
    def post(self):
        jsonstring = self.request.body
        print 'JSON STRING RECV '+jsonstring
        jsonobject = json.JSONDecoder().decode(jsonstring);
        
        command = jsonobject['command']
        self.response.headers['Content-Type']='application/json'

        if command is not None:
            response_json = json.JSONEncoder().encode({'status':'fail'})
            if command == 'register':
                response_json = self.register_participant();
            
                
        print response_json  
        self.response.write(response_json);
        
        
    def get(self): 
        self.response.headers['Content-Type']='application/json'
        response_json = json.JSONEncoder().encode({'status':'fail'});
        self.response.write(response_json)

app = webapp2.WSGIApplication([('/SliderPage', SliderPage)],
                              debug=True)
