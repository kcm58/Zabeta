import api
from google.appengine.ext import db
from datamodel import University

class list(api.api):
    public={"list":True}

    def list(self):
        return University.gql("")