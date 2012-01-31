import api

class measure(api.api):
    public={}
    def get(self):
        return ["one","two","three"]