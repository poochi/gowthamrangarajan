## This is the server side implementation for few of the games i've written
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

    def pick_random_question(self):
        #qkey  = QuestionKind('EnglishQuestion');
        attempt = 0;
        questionEntities = []
        while(len(questionEntities)== 0 and attempt <10):
            questionEntities = QuestionKind.query().filter(QuestionKind.randomID >= random.random()).fetch(1);
            
            attempt+=1;
        if attempt == 10:
            return ;
        print questionEntities
        return [questionEntities[0].qid,questionEntities[0].question,questionEntities[0].hints];
        
    def register_participant(self):
        CONTEST_TIME = 180
        EVAL_TIME = 120
        BUFFER_TIME = 0    
        p = datetime.datetime.now();       
        
        #always starts at 3:00 etc.,
        self.total_contest_duration = 30
        delta = self.total_contest_duration - (p.minute*60 + p.second)%self.total_contest_duration

        self.nextconteststart = p + datetime.timedelta(seconds = delta);
        contesttime = str(delta)
        

        contestKey = ndb.Key('ContestDetailsKind',self.nextconteststart.ctime());
        res = ContestDetailsKind.query_contestDetails(contestKey).fetch(1);
        if len(res) == 1:
            #Query the question from the QKind using id

            ###Doesnt work investigate 
            #qkey  = ndb.Key(QuestionKind,int(res[0].qid))
            #print int(res[0].qid)
            #q = qkey.get()

            q = QuestionKind.query().filter(QuestionKind.qid == res[0].qid).fetch(1);
            
            print q
            q=q[0];
            
            if q == None :
                response_json = json.JSONEncoder().encode({'status':'fail','reason':'StaleContestTable or Non-sync Question Table '})
            else:
                response_json = json.JSONEncoder().encode({'status':'success','reason':'Question Picked','question':q.question,'time':contesttime,'hints':q.hints,'questionid':res[0].qid,'contestno':res[0].contestno})
            #else:
            #    response_json = json.JSONEncoder().encode({'status':'fail','reason':'ClashingQID'})
                

        else:
            [qid,ques,hints]= self.pick_random_question();
            if qid == None:
                response_json = json.JSONEncoder().encode({'status':'fail','reason':'Random QpickFailed'})
            else:                
                
                cd = ContestDetailsKind(parent = ndb.Key('ContestDetailsKind',self.nextconteststart.ctime()),qid=qid,contestno=15)
                cd.put();
                response_json = json.JSONEncoder().encode({'status':'success','reason':'Created a new Contest','question':ques,'time':contesttime,'hints':hints,'questionid':qid,'contesttime':contesttime})
            
            
        
        return response_json;

    def update_participant_scores(self):
        #add to list/ update details
        print 'update_participant_scores'

        jsonstring = self.request.body
        jsonobject = json.JSONDecoder().decode(jsonstring);
        
        pname = jsonobject['name'];
        command = jsonobject['command'];
        questionid = int(jsonobject['questionid']);
        scr = int(jsonobject['score']);
        pid = jsonobject['participantid']
        #qid = jsonobject['qid']
        
        ld = QuestionLeaderBoardKind(parent = ndb.Key('QuestionLeaderBoardKind',str(questionid)+str(pid)),participantid=pid,
                                                      participantname=pname,score=scr,qid=questionid)
        ld.put();
        response_json = json.JSONEncoder().encode({'status':'success','reason':'Added to QuestionLeader Board/Updated participant Score','score':scr,'time':4});
        return response_json
        


    def retrieve_rank(self):
        jsonstring = self.request.body
        jsonobject = json.JSONDecoder().decode(jsonstring);
        myid = jsonobject['participantid']
        qid = jsonobject['questionid']
        
        
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
            if command == 'updatetable':
                
            
                
        print response_json  
        self.response.write(response_json);
        
        
    def get(self): 
        self.response.headers['Content-Type']='application/json'
        response_json = json.JSONEncoder().encode({'status':'negative'});
        self.response.write(response_json)

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)

            
    

