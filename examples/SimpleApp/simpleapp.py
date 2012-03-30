import webapp2
from google.appengine.api import users

### NOTE:
### Each of these works as expected if the datastore is cleared and
### repopulated. Bad things happen if the datastore is not
### repopulated.

######################################################################
### db.ReferenceProperty with db.Model
######################################################################
# from google.appengine.ext import db

# class Category(db.Model):
#     name = db.StringProperty()
#     # implicit 'events' property is the set of all events with
#     # this object as its category

# class Event(db.Model):
#     description = db.TextProperty()
#     category = db.ReferenceProperty(Category,
#                                     collection_name='events')


######################################################################
### db.ReferenceProperty with polymodel.PolyModel
######################################################################
# from google.appengine.ext import db
# from google.appengine.ext.db import polymodel

# class Base(polymodel.PolyModel):
#     pass

# class Category(Base):
#     name = db.StringProperty()
#     # implicit 'events' property is the set of all events with
#     # this object as its category

# class Event(db.Model):
#     description = db.TextProperty()
#     category = db.ReferenceProperty(Category,
#                                     collection_name='events')



######################################################################
## db.ReverseReferenceProperty with db.MoraModel
######################################################################
# from mora import db

# class Category(db.MoraModel):
#     name = db.StringProperty()
#     events = db.ReverseReferenceProperty('Event', 'category')

# class Event(db.MoraModel):
#     description = db.TextProperty()
#     category = db.ReferenceProperty(Category)


######################################################################
## db.ReverseReferenceProperty with db.MoraPolyModel
######################################################################
from mora import db

class Base(db.MoraPolyModel):
    pass

class Category(Base):
    name = db.StringProperty()
    events = db.ReverseReferenceProperty('Event', 'category')

class Event(db.MoraModel):
    description = db.TextProperty()
    category = db.ReferenceProperty(Category)



class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('I\'m alive!')
        else:
            self.redirect(users.create_login_url(self.request.uri))



class PopulateHandler(webapp2.RequestHandler):
    def clear(self, kind):
        # we only need the low-level api for this method
        from google.appengine.api import datastore

        # robustly delete the entities 500 elements at a time
        batch_size = 500
        query = datastore.Query(kind=kind, keys_only=True)
        results = query.Get(batch_size)
        while results:
            datastore.Delete(results)
            results = query.Get(batch_size)

    def get(self):
        self.clear('Event')
        self.clear('Category')

        category1 = Category(name='Concert').put()

        category2 = Category(name='Film').put()


        event1 = Event(description='Modest Mouse at the Orpheum',
                       category=category1).put()

        event2 = Event(description='How to Destroy Angels at the Orpheum',
                       category=category1).put()

        event3 = Event(description='The Big Lebowski at the Orpheum',
                       category=category2).put()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Populate successful.')


app = webapp2.WSGIApplication([
        ('/', MainPage),
        ('/populate', PopulateHandler)], debug=True)
