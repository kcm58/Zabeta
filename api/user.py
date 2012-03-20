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
        self.redirect("/")
        return "success"

    def getTasks(self):
        return datamodel.Task.gql("where delegates=KEY(:1)",self.user["id"])

    def getCurrentCourses(self):
        return datamodel.CourseOffering.gql("where instructor=KEY(:1)",self.user["id"])
