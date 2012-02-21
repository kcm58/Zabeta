import api
from google.appengine.ext import db

class University(api.api):
    public={"list":True}

    def list(self):
        return db.GqlQuery("select * from University")