import api
from google.appengine.ext import db
import datamodel

class Course(api.api):
    public={"list":True}

    def list(self):
        return datamodel.Course.gql("")