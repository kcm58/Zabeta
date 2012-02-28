import api
import datamodel

class user(api.api):
    public={"get":True,
            "logout":True,
            "getTasks":True,
            "getCurrentCourses":True,}

    def get(self):
        return self.user

    def logout(self):
        self.destroy_session()
        return "success"

    def getTasks(self):
        return datamodel.Task.get(self.user["tasks"])

    def getCurrentCourses(self):
        return datamodel.CourseOffering.gql("")#where instructor=KEY(:1),self.user["id"])
