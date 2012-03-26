import api
import datamodel

class user(api.api):
    public={"get":True,
            "logout":True,
            "getTasks":True,
            "getCurrentCourses":True,}

    def get(self):
        # TODO: we should return all of the initial data in one request
        #       (howerver that's done?)
        # ret = {
        #   "user": self.user,
        #   "university":
        #     datamodel.University.get_by_id(self.user['university'])
        # }
        # return ret
        return self.user

    def logout(self):
        self.destroy_session()
        self.redirect("/")
        return "success"

    #We are only pull out tasks where this user is a delegate
    #Filtering by university and program isn't needed.
    def getTasks(self):
        return datamodel.Task.gql("where delegates=KEY(:1)",self.user["id"])

    #Same here,  filtering by university and program isn't needed.
    def getCurrentCourses(self):
        return datamodel.CourseOffering.gql("where instructor=KEY(:1)",self.user["id"])
