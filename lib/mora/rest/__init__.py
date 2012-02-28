#     (c) 2012 James Dean Palmer
#     Mora may be freely distributed under the Apache 2.0
#     licence.  You may obtain a copy of this license at
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     For all details and coumentation:
#     http://jdpalmer.github.com/mora

# *Mora* provides restful services and richer JSON support for Google
# App Engine (GAE). Mora intends to be lightweight and unobtrusive.

### Motivation

# This module provides a dispatcher and REST handler class you can use
# to make your own RESTful graphs. A RESTful graph API has an
# organization similar to Facebook's graph api and is a bit
# different than the default way most other frameworks implement REST.
# 
# To get a Student object with Mora you might send a GET request to:
#
#     /graph/ag9kZXZ-YmVhbmdyaW5kZXJyCgsSBFVzZXIYAQw
#
# You don't specify that you want a user resource because GAE already
# has this embedded in the key.  You can then use PUT and DELETE http
# verbs to update and remove the object.  Now if you want to get a
# list of courses the user is in, you send a GET to:
#
#     /graph/ag9kZXZ-YmVhbmdyaW5kZXJyCgsSBFVzZXIYAQw/courses
#
# And if you want to add a course, you send a POST to the same URL.
# There are no nested resource calls because they are unneccessary.

### Dependencies

# We import some standard modules and also Google App Engine's `db`
# and `polymodel` modules.  We have to dig at GAE's guts a bit to
# shoehorn in better per type JSON support but most of this can be
# accomplished with simple subclassing.
import logging
import sys
import inspect
from mora import db
import session

# GAE supports a couple of versions of Python and the GAE environment.
# We will try to use the latest modules and then use `ImportError`
# exceptions to select older variations.
try:
    import json
except ImportError:
    from django.utils import simplejson as json

try:
    import webapp2 as webapp
except ImportError:
    from google.appengine.ext import webapp


### Decorators

# `show`, `update`, and `delete` are the only named REST action
# methods in `RestHandler`.  All other REST actions must be
# accomplished with special method decorators.  These decorators
# attach REST HTTP verbs to functions.
#
# To setup an index for courses, we could write:
#
#      @rest_index("courses")
#      def course_list(self):
#          # return the courses..
def rest_index(keyword):
    def wrap(f):
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        setattr(wrapped, "_mora_verb", ("GET " + keyword, f.func_name))
        return wrapped
    return wrap


# Similarly we might want to be able to add a new course.  rest_create
# attaches the POST verb to a function so that we can write:
#
#      @rest_create("courses")
#      def course_create(self):
#          # create a course..
def rest_create(keyword):
    def wrap(f):
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        setattr(wrapped, "_mora_verb", ("POST " + keyword, f.func_name))
        return wrapped
    return wrap


# And there may be some occasions where you need to take some special
# action on an item that doesn't fall into one of the usual 'index',
# 'create', 'update', 'destroy', or 'show' actions.  These should be
# annotated with the rest_action decorator:
#
#      @rest_create("like")
#      def like(self):
#          # execute a like action on the user
def rest_action(keyword):
    def wrap(f):
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        setattr(wrapped, "_mora_verb", ("POST " + keyword, f.func_name))
        return wrapped
    return wrap


### Dispatcher Exceptions

# DispatchErrors may be thrown when something goes wrong and will be
# caught at the RequestHandler stage.  When you throw an error you
# should set the code and message.  Some standard codes and messages
# that Mora throws internally include:
#
# * 400: InvalidHttpVerb
# * 400: InvalidUri
# * 404: ResourceNotFound
# * 405: UnsupportedHttpVerb
class DispatchError(Exception):

    def __init__(self, code=None, message=None):
        super(DispatchError, self).__init__()
        self.code = code
        self.message = message

### REST Dispatcher

# The `RestDispatcher` is a request handler that gets passed to
# webapp.  We then spawn our custom RestHandlers from here.
#Michael Brooks - RestDispatcher impalments sesison instead of a RequestHandler
class RestDispatcher(session.session):

    base_path = ""
    rest_handlers = {}


    # We setup the dispatcher with a path it should use and a list of
    # RestHandlers connected to specific models.
    @classmethod
    def setup(cls, path, handlers):
        cls.base_path = path
        for rest_handler in handlers:
            cls.connect(rest_handler)


    # We pass back a reference to the base_path and this class as the
    # routing pair.
    @classmethod
    def route(cls):
        return (cls.base_path + "/.*", RestDispatcher)


    @classmethod
    def connect(cls, rest_handler):
        model = rest_handler.model
        cls.rest_handlers[model.class_name()] = rest_handler

        verbs = {}
        # When we connect RestHandler subclasses to this class we also
        # scan their methods looking for methods that were decorated
        # as rest actions.
        for k, v in inspect.getmembers(rest_handler):
            if hasattr(v, "_mora_verb"):
                verbs.update([getattr(v, "_mora_verb")])
        logging.info(verbs)

        # We also include the standard rest methods.
        verbs.update({"GET __self__": "show",
                      "DELETE __self__": "destroy",
                      "PUT __self__": "update"})

        logging.info(verbs)
        # We then attach this list of actions to the class.
        setattr(rest_handler, "_mora_verbs", verbs)


    def __init__(self, request=None, response=None):
        if (request is None) and (response is None):
            super(RestDispatcher, self).__init__()
        else:
            super(RestDispatcher, self).__init__(request, response)


    # The standard http verb methods are rerouted to the action method.
    def get(self, *_):
        self.action('GET')


    def put(self, *_):
        self.action('PUT')


    def delete(self, *_):
        self.action('DELETE')


    def post(self, *_):
        self.action('POST')


    def action(self, act, exceptions=False):

        # The action method handles exceptions by recursively calling
        # itself such that we have one spot that we can catch
        # `DispatchError`s.
        if not exceptions:
            try:
                self.action(act, exceptions=True)
            except DispatchError as error:
                self.response.set_status(error.code)
                self.response.out.write("Error " + str(error.code))
            return

        # We also support a special `_method` argument to change the
        # HTTP verb being used.  This is to support browsers with poor
        # support for making AJAX calls with arbitrary HTTP verbs and
        # other oddball cases.
        if self.request.get("_method"):
            act = self.request.get("_method")
            if not(act in ["GET", "POST", "DELETE", "PUT"]):
                raise DispatchError(400, "InvalidHttpVerb")

        # In order to respond to a request, we have to build a path
        # and remove the `base_path` prefix from it.
        path = self.request.path
        if (path.startswith(self.base_path)):
            path = path[len(self.base_path) + 1:]
        path = list(path.split('/'))
        path.reverse()

        # The key is now the first element in the path.
        key = path.pop()

        # We obtain the model instance from the key.
        try:
            model = db.get(key)
        except db.BadKeyError:
            raise DispatchError(404, "ResourceNotFound")

        model_name = model.class_name()

        # We then can use the model to create an appropriate handler.
        if model_name in self.rest_handlers:
            rest_handler = self.rest_handlers[model_name](model, self.request, self.response)
            rest_handler.setup()
        else:
            raise DispatchError(404, "ResourceNotFound")

        # If nothing follows the key, we assume the action is on the
        # current object ("__self__").  Otherwise we capture a keyword
        # that represents a path or alternate action to take.
        if len(path) == 0:
            keyword = "__self__"
        else:
            keyword = path.pop()
            if len(path) != 0:
                raise DispatchError(400, "InvalidUri")

        # We then use the HTTP verb and keyword to lookup the method
        # to call.
        action_key = act + ' ' + keyword
        if action_key in rest_handler._mora_verbs:
            action_method = rest_handler._mora_verbs[action_key]
            result = getattr(rest_handler, action_method)()
        else:
            logging.info(action_key)
            raise DispatchError(405, "UnsupportedHttpVerb")

### RestHandler

# The RestHandler is attached to the model, request, and response.
# You can override the provided `show`, `update` and `delete` methods
# or create new methods.
class RestHandler(object):

    _mora_verbs = {}

    def __init__(self, model, request, response):
        self.model = model
        self.request = request
        self.response = response
        self.params = {}
        for arg in self.request.arguments():
            self.params[arg] = self.request.get(arg)

    def setup(self):
        pass

    # REST methods should be very lightweight.  Use the as_json method
    # to push business logic into the model.  Here are some example
    # implementations for each method:

    # Example:
    #
    #     def show(self):
    #       self.response.out.write(self.model.to_json())
    def show(self):
        raise DispatchError(405, "UnsupportedHttpVerb")

    # Example:
    #
    #     def update(self):
    #       self.model.from_json(self.params)
    def update(self):
        raise DispatchError(405, "UnsupportedHttpVerb")

    # Example:
    #
    #     def destroy(self):
    #       self.model.delete()
    #       self.response.out.write({})
    def destroy(self):
        raise DispatchError(405, "UnsupportedHttpVerb")
