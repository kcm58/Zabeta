import api

class init(api.api):
    public={"get":True}

    def get(self):
        return self.user