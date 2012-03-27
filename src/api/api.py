import session

class api(session.session):
    public={}

    def __init__(self,request,response):
        self.request=request
        self.response=response
        session.session.__init__(self,request,response)

    def getPublic(self):
        return self.public