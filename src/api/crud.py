from mora.rest import RestHandler,rest_create,rest_index,DispatchError
#from mora import db
from google.appengine.ext import db
import datamodel
import datetime
import json
import session
import google.appengine.ext
import http_header

class CrudSession(RestHandler,session.session):
  
    def __init__(self, model, request, response):
        RestHandler.__init__(self,model,request,response)
        session.session.__init__(self,request,response)
        self.key=str(model.key())
        
    def setup(self):
        #Check if an exception was thrown.
        self.isAuthenticated()
        
        model=self.model
        model_name=self.model.class_name()
        #User Access Control DO NOT REMOVE!
        #University is except,  anyone can access this collection
        #Check to make sure the program and university match what the user has access to.

        #University is a speical case,  it is the name of the Zone
        if model_name == "University":
            #Check to make sure the user uses this university
            #This is a special case
            if str(model.key()) != self.university_id:
                raise DispatchError(403, "ResourceNotAllowed")
        #Program is another special case,  this is the name of or Relm within the Zone.
        elif model_name == "Program":
            if str(model.key()) != self.program_id or str(model.university.key()) != self.university_id:
                raise DispatchError(403, "ResourceNotAllowed")
        elif model_name == "User":
            #the self.key value is the model.key(),  but model.key() doesn't work...
            #Grab this user's authentication record and see if they belong to this Program
            ar=datamodel.AuthenticationRecord.gql("where user=key(:1)",self.key).fetch(1)[0]
            found_program=False
            for p in ar.programs:
                if p in self.user['programs']:
                    found_program=True
                    break
            #If the user isn't modifying their own record 
            #and the user accessing this api call isn't an administrator over the user
            #Then the user can't access this "User" record
            if str(self.key) != self.user['id'] and not found_program:
                raise DispatchError(403, "ResourceNotAllowed")
        #we assume that we have a "program" and "university" for every other collection.
        else:
            if (str(model.program.key()) != self.program_id or str(model.university.key()) != self.university_id):
                raise DispatchError(403, "ResourceNotAllowed")

class CrudRevision(CrudSession):
    def duplicate(self,src,dest):
        #iterate over each parameter specified in the select
        for key in src._all_properties:
            if key!="id":
                val=getattr(src,"_"+key)
                setattr(dest,key,val)    
#            t=type(var)
#            if t is list:
#                if len(var) and type(var[0]) is db.Key:
#                    ids=[]
#                    for v in var:
#                        ids.append(str(v))
#                    element[key]=ids
#            else:
#                element[key]=str(var)
#        return element

    def version_save(self,new_ver):
        name=new_ver.class_name()
        collection=getattr(datamodel,name) 
        
        v=collection()
        self.duplicate(new_ver,v)
        v.commit_user=self.user['id']
        v.commit_program=self.program_id
        v.commit_university=self.university_id
        #This is a new minor revision
        v.commit_minor+=1
        v.commit_timestamp=datetime.datetime.now()
        v.save()              

#A user is NOT revisioned,  and does not use version_interface
class User(CrudSession):
      
    model = datamodel.User
      
    def show(self):
        self.response.out.write(self.model.to_json())
          
    def update(self):
        self.model.from_json(self.params)

#Authentication methods and and records are also not versioned        
class AuthenticationMethod(CrudSession):

    model = datamodel.AuthenticationMethod
    
    model = datamodel.Outcome

    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)

class AuthenticationRecord(CrudSession):

    model = datamodel.AuthenticationRecord
    
    model = datamodel.Task

    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())
        

    def update(self):
        self.model.from_json(self.params)


class Outcome(CrudRevision):

    model = datamodel.Outcome

    def show(self):
        self.response.out.write(self.model.to_json())
        

    def update(self):
        #Override the base values. 
        self.params['program']=self.program_id
        self.params['university']=self.university_id
        new_outcome=datamodel.Outcome()
        new_outcome.from_json(self.params)
        #Populate the response
        self.model.outcomes.append(new_outcome)
        self.version_save(self.model)
     

class Objective(CrudRevision):

    model = datamodel.Objective
    
    def show(self):
        self.response.out.write(self.model.to_json())
        

    def update(self):
        self.model.from_json(self.params)

    @rest_create("outcome")
    def response_new(self):
        #Override the base values. 
        self.params['program']=self.program_id
        self.params['university']=self.university_id
        new_outcome=datamodel.Outcome()
        new_outcome.from_json(self.params)
        #Populate the response
        self.model.outcomes.append(new_outcome)
        self.version_save(self.model)

class Task(CrudRevision):

    model = datamodel.Task
    
    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)

    @rest_create("response")
    def response_new(self):
        #Populate the response
        self.model.response=str(self.params)
        self.model.save()

class AssessmentTask(Task):
  
    model = datamodel.AssessmentTask

class CourseTask(Task):
  
    model = datamodel.CourseTask 

class Course(CrudRevision):

    model = datamodel.Course

    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)

class CourseOffering(CrudRevision):

    model = datamodel.CourseOffering

    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)
        
class OutcomeSupport(CrudRevision):

    model = datamodel.OutcomeSupport

        
#A user is NOT revisioned,  and does not use version_interface
class Semseter(CrudRevision):

    model = datamodel.Semester

    def show(self):
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)

class University(CrudRevision):

    model = datamodel.University

    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())

    @rest_index("programs")
    def program_list(self):
      programs = []
      for prog in datamodel.Program.all().fetch(1000):
        programs.append(prog.as_json())
      self.response.out.write(json.dumps(programs))

    @rest_index("semesters")
    def semester_list(self):
      semesters = []
      for prog in datamodel.Semester.all().fetch(1000):
        semesters.append(prog.as_json())
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(json.dumps(semesters))

    @rest_index("users")
    def user_list(self):
      users = []
      for prog in datamodel.User.all().fetch(1000):
        users.append(prog.as_json())
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(json.dumps(users))

class Program(CrudRevision):

    model = datamodel.Program

    def show(self):
        self.response.out.write(self.model.to_json())
        
class Minutes(CrudRevision):

    model = datamodel.Minutes
    
    def show(self):
        self.response.out.write(self.model.to_json())
        
    def update(self):
        self.model.from_json(self.params)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())
