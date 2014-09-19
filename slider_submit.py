#slider submit.py
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


class SliderPageSubmit(webapp2.RequestHandler):
        
    def update_participant_scores(self):
    	#add to contest list
        #add to list/ update details
        print 'update_participant_scores'

        jsonstring = self.request.body
        jsonobject = json.JSONDecoder().decode(jsonstring);
        user = users.get_current_user()
        command = jsonobject['command'];
        questionid = int(jsonobject['questionid']);
        scr = int(jsonobject['score']);
        assert(command !=None);
        assert(questionid !=None);
        assert(type(scr) == int);
        
        if user:
        	pname = user.nickname();            
        else:
        	print 'user authenticating failed';
        	response_json = json.JSONEncoder().encode({'status':'failed','reason':'login','url':users.create_login_url('/')});
        	return;

        #qid = jsonobject['qid']
        pid = hash(pname);
        
        ld = QuestionLeaderBoardKind(parent = ndb.Key('QuestionLeaderBoardKind'),participantid=pid,
                                                      participantname=pname,score=scr,qid=questionid)
        ld.put();

        response_json = json.JSONEncoder().encode({'status':'success','reason':'Added to QuestionLeader Board/Updated participant Score','score':scr,'time':4});
        return response_json
        


    def retrieve_rank(self):
    	#query neighbours and top guys with score
        jsonstring = self.request.body
        jsonobject = json.JSONDecoder().decode(jsonstring);
        
        qid = jsonobject['questionid']
        if user:
        	pname = user.nickname();            
        else:
        	print 'user authenticating failed';
        	response_json = json.JSONEncoder().encode({'status':'failed','reason':'login','url':users.create_login_url('/')});
        	return;
        
        
        #q = QuestionLeaderBoardKind.query().order(ndb.IntegerProperty('score'))
        qry = ndb.gql("SELECT * FROM QuestionLeaderBoardKind WHERE qid = "+str(qid)+" ORDER BY score")
        
        entries = qry.fetch(1000);
        rank = 0
        neighbourrankmemory = 10; #exculding me #5 top  5 next
        neighbourranks = [];

        prank = 1000
        totranks = len(entries);
        participantfound = False;
        times = 0;
        data = [];
        for each in entries:
            rank+=1;
            if participantfound == True:
                times+=1;
                if times >neighbourrankmemory/2:
                    break;
            if rank >neighbourrankmemory/2 and participantfound == False:
                    neighbourranks.remove(neighbourranks[0]);
            neighbourranks.append(each.participantid);
                
                
            
            if each.participantid == myid:
                prank = rank+1;
                participantfound = True;
            else:
                if rank<10:                
                    data.append(each.participantname);
        
        response_json = json.JSONEncoder().encode({'status':'success','reason':'retrive 1000 ranks','rank':prank,
                                  'neighbours':neighbourranks,'Toppers':data});
        return response_json;
        


    
        
    def post(self):
        jsonstring = self.request.body
        print 'JSON STRING RECV '+jsonstring
        jsonobject = json.JSONDecoder().decode(jsonstring);
        
        command = jsonobject['command']
        self.response.headers['Content-Type']='application/json'

        if command is not None:
            response_json = json.JSONEncoder().encode({'status':'fail'})            
            elif command == 'updatescore':
                response_json = self.update_participant_scores();
            elif command == 'obtainresult':
                response_json = self.retrieve_rank();
            
                
        print response_json  
        self.response.write(response_json);
        
        
    def get(self): 
        self.response.headers['Content-Type']='application/json'
        response_json = json.JSONEncoder().encode({'status':'negative'});
        self.response.write(response_json)

app = webapp2.WSGIApplication([('/SliderPageSubmit', SliderPageSubmit)],
                              debug=True)
