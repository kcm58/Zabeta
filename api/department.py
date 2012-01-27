import api

class department(api.api):
    public={"get":True}
    def get(self):
        self.output=["Computer Science","Engineering","Whatever"]