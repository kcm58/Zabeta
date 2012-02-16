import api
from google.appengine.ext import db

class University(api.api):
    public={"list":True}

    def list(self):
        ret=[]
        u=db.GqlQuery("select * from University")
        u_list=u.fetch(2048)
        for i in u_list:
            ret.append({"id":i.key().__str__() ,
                        "name":i.name})
        return {"University":ret}