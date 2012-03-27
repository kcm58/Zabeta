from mora.rest import RestHandler,rest_create,rest_index
from mora import db
import datamodel
import json

class Outcome(RestHandler):

    model = datamodel.Outcome

    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)

class Task(RestHandler):

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

class CourseTask(RestHandler):

    model = datamodel.CourseTask

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

class User(RestHandler):

    model = datamodel.User

    def show(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)

class University(RestHandler):

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
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(self.model.to_json())
