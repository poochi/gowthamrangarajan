from google.appengine.ext import ndb
from google.appengine.api import users

class QuestionKind(ndb.Model):
    question = ndb.StringProperty();
    wordlist = ndb.StringProperty(repeated=True);
    hints =ndb.StringProperty(repeated=True)
    randomID =  ndb.FloatProperty();
    qid = ndb.IntegerProperty();

    @classmethod
    def query_kind(book,ancestor_key):
        return book.query(ancestor_key);

class QuestionLeaderBoardKind(ndb.Model):
    qid = ndb.IntegerProperty();    
    score = ndb.IntegerProperty();
    participantname = ndb.StringProperty()
    participantid = ndb.StringProperty()


    
class ContestDetailsKind(ndb.Model):    
    contestquestion =ndb.StringProperty();

    contestno = ndb.IntegerProperty();
    date = ndb.DateTimeProperty(auto_now_add=True);
    qid =  ndb.IntegerProperty();


    @classmethod
    def query_contestDetails(book,ancestor_key):
        return  book.query(ancestor=ancestor_key);
