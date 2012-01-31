import api

class department(api.api):
    public={"get":True}
    def get(self):
        return ["Computer Science","Engineering","Whatever"]