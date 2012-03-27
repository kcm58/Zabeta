from mora.rest import RestHandler,rest_create,rest_index
from mora import db
import datamodel
<<<<<<< HEAD
import datetime
=======
import json
>>>>>>> 8f3579e407d23c5dac0037841f5d6f4f2282996f

#A user is NOT revisioned,  and does not use version_interface
class User(RestHandler):
      
    model = datamodel.User
      
    def show(self):
        self.response.out.write(self.model.to_json())
          
    def update(self):
        self.model.from_json(self.params)

<<<<<<< HEAD
#Authentication methods and and records are also not versioned        
class AuthenticationMethod(RestHandler):

    model = datamodel.AuthenticationMethod
    
=======
    model = datamodel.Outcome

>>>>>>> 8f3579e407d23c5dac0037841f5d6f4f2282996f
    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)

class AuthenticationRecord(RestHandler):

<<<<<<< HEAD
    model = datamodel.AuthenticationRecord
    
=======
    model = datamodel.Task

>>>>>>> 8f3579e407d23c5dac0037841f5d6f4f2282996f
    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())
<<<<<<< HEAD
        
=======

>>>>>>> 8f3579e407d23c5dac0037841f5d6f4f2282996f
    def update(self):
        self.model.from_json(self.params)


<<<<<<< HEAD
class Outcome(RestHandler):

    model = datamodel.Outcome
    
=======
class AssessmentTask(Task):

    model = datamodel.AssessmentTask

>>>>>>> 8f3579e407d23c5dac0037841f5d6f4f2282996f
    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())
<<<<<<< HEAD
        
    def update(self):
        self.model.from_json(self.params)
        #Override the base values. 
        self.params['program']=self.program_id
        self.params['university']=self.university_id
        new_outcome=datamodel.Outcome()
        new_outcome.from_json(self.params)
        #Populate the response
        self.model.outcomes.append(new_outcome)
        self.version_save(self.model)        

class Objective(RestHandler):

    model = datamodel.Objective
    
    def show(self):
        self.response.out.write(self.model.to_json())
        
=======

>>>>>>> 8f3579e407d23c5dac0037841f5d6f4f2282996f
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
<<<<<<< HEAD
        self.model.outcomes.append(new_outcome)
        self.version_save(self.model)

class Task(RestHandler):

    model = datamodel.Task
    
=======
        self.model.response=str(self.params)
        self.model.save()

class CourseTask(RestHandler):

    model = datamodel.CourseTask

>>>>>>> 8f3579e407d23c5dac0037841f5d6f4f2282996f
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
<<<<<<< HEAD

class AssessmentTask(Task):
  
    model = datamodel.AssessmentTask

class CourseTask(Task):
  
    model = datamodel.CourseTask 
=======
>>>>>>> 8f3579e407d23c5dac0037841f5d6f4f2282996f

class Course(RestHandler):

    model = datamodel.Course

    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)

class CourseOffering(RestHandler):

    model = datamodel.CourseOffering

    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)
        
class OutcomeSupport(RestHandler):

    model = datamodel.OutcomeSupport

<<<<<<< HEAD
=======
class User(RestHandler):

    model = datamodel.User

>>>>>>> 8f3579e407d23c5dac0037841f5d6f4f2282996f
    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)        
        
#A user is NOT revisioned,  and does not use version_interface
class Semseter(RestHandler):

    model = datamodel.Semester

    def show(self):
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)

class University(RestHandler):
<<<<<<< HEAD
    
=======

>>>>>>> 8f3579e407d23c5dac0037841f5d6f4f2282996f
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

class Program(RestHandler):

    model = datamodel.Program

    def show(self):
<<<<<<< HEAD
        self.response.out.write(self.model.to_json())
        
class Minutes(RestHandler):

    model = datamodel.Minutes
    
    def show(self):
        self.response.out.write(self.model.to_json())
        
    def update(self):
        self.model.from_json(self.params)
=======
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())
>>>>>>> 8f3579e407d23c5dac0037841f5d6f4f2282996f
