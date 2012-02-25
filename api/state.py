import api
import session

class state(api.api):
    public={"get":True,
            "logout":True}

    def get(self):
        return self.user

    def logout(self):
        self.destroy_session()