#     (c) 2012 James Dean Palmer
#     (c) 2007 Google Inc.
#     Mora may be freely distributed under the Apache 2.0
#     licence.  You may obtain a copy of this license at
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     For all details and coumentation:
#     http://jdpalmer.github.com/mora

# *Mora* provides restful services and richer [JSON][json] support for
# [Google App Engine][gae] (GAE). Mora intends to be lightweight and
# unobtrusive.
# [gae]: http://code.google.com/appengine/ "Google App Engine"
# [json]: http://www.json.org/ "JavaScript Object Notation"

### Motivation

# One of the most important things that Mora adds to GAE models and
# properties is a mechanism for generating JSON.  I have adopted
# [Rails][rails]-style `to_json` and `as_json` methods and have
# specifically avoided placing this logic in a [JSONEncoder][jsone]
# subclass.  There's a few reasons for this - the first is that such a
# subclass would have to know about all of App Engine's types and
# models.  If you add new types and classes you have to modify or
# further subclass the encoder. And if third-party libraries use their
# own JSONEncoder subclass, you have the unenviable task of patching
# the variations to work together. There's also a real danger in
# putting business logic in your encoder because the easy to place to
# filter and manipulate JSON properties is where they are being
# generated.  Last time I checked there was no
# Model-View-Controller-JSONEncoder paradigm.  The JSONEncoder is the
# wrong place to make view decisions or business logic decisions.
#
# Rails has split the JSON rendering process into [two parts][julian].
# A method called `as_json` is used to build a representation made of
# core JSON-types.  `as_json` is the smart half of the equation and
# belongs to the Model and can make business logic decisions.
# `to_json` then calls the json encoder and that's pretty much all it
# does.
#
# Mora adopts this philoshopy and adds `as_json` to GAE's models *and*
# types.  If you add new models and types and also add the `as_json`
# method it will all just work (TM).
# [julian]: http://jonathanjulian.com/2010/04/rails-to_json-or-as_json/ "Rails to_json or as_json?"
# [rails]: http://rubyonrails.org/ "Ruby on Rails"
# [jsone]: http://docs.python.org/library/json.html "JSON in Python"

### Dependencies

# We import some standard modules and also Google App Engine's `db`
# and `polymodel` modules.  We have to dig at GAE's guts a bit to
# shoehorn in better per type JSON support but most of this can be
# accomplished with simple subclassing.
import logging
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.api import datastore

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

### Keys and Errors

# These remain unchanged so we simply import them into this namespace.

Error = db.Error
BadValueError = db.BadValueError
BadPropertyError = db.BadPropertyError
BadRequestError = db.BadRequestError
EntityNotFoundError = db.EntityNotFoundError
BadArgumentError = db.BadArgumentError
QueryNotFoundError = db.QueryNotFoundError
TransactionNotFoundError = db.TransactionNotFoundError
Rollback = db.Rollback
TransactionFailedError = db.TransactionFailedError
BadFilterError = db.BadFilterError
BadQueryError = db.BadQueryError
BadKeyError = db.BadKeyError
InternalError = db.InternalError
NeedIndexError = db.NeedIndexError
ReferencePropertyResolveError = db.ReferencePropertyResolveError
Timeout = db.Timeout
CommittedButStillApplying = db.CommittedButStillApplying
ValidationError = db.ValidationError

Key = db.Key
Category = db.Category
Link = db.Link
Email = db.Email
GeoPt = db.GeoPt
IM = db.IM
PhoneNumber = db.PhoneNumber
PostalAddress = db.PostalAddress
Rating = db.Rating
Text = db.Text
Blob = db.Blob
ByteString = db.ByteString
BlobKey = db.BlobKey

NotSavedError = db.NotSavedError
KindError = db.KindError
PropertyError = db.PropertyError
DuplicatePropertyError = db.DuplicatePropertyError
ConfigurationError = db.ConfigurationError
ReservedWordError = db.ReservedWordError
DerivedPropertyError = db.DerivedPropertyError

Query = db.Query
get = db.get

### Properties

# Since Python is duck-typed, there's really no reason to change the
# implementation of db.Property even though we are adding `as_json` to
# all of its subclasses.  We add it here to mirror the original
# definition.
Property = db.Property

# We change the other core properties by simply subclassing them with
# the same name in a different namespace.  This makes them drop-in
# replacements for the original properties but they also have the new
# `as_json` method.
class StringProperty(db.StringProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    return str(value)


class BooleanProperty(db.BooleanProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    return bool(value)


class IntegerProperty(db.IntegerProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    try:
      return long(value)
    except:
      return None


class FloatProperty(db.FloatProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    return float(value)


class TextProperty(db.TextProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    return str(value)


class ByteStringProperty(db.ByteStringProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    return str(value)


class EmailProperty(db.EmailProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    return str(value)


class PostalAddressProperty(db.PostalAddressProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    return str(value)


# There is no standard for date representation in JSON.  We use
# ISO8601 for representing time which is pretty common.
class DateTimeProperty(db.DateTimeProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    return value.isoformat("T") + "+00:00"


class DateProperty(db.DateProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    return value.isoformat("T") + "+00:00"


class TimeProperty(db.TimeProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    return value.isoformat("T") + "+00:00"


class ListProperty(db.ListProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    # TODO: Flatten each item inside the list
    return value


class StringListProperty(db.StringListProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    # TODO: Flatten each item inside the list
    return value


class UserProperty(db.UserProperty):

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    if value is None:
      return {}
    else:
      return {"nickname": value.nickname(),
              "email": value.email(),
              "user_id": value.user_id(),
              "federated_identity": value.federated_identity(),
              "federated_provider": value.federated_provider()}

### ReferenceProperty

# The `ReferenceProperty` likewise has a simple `as_json` method
# similar to the properties we defined above, but I'm taking this
# opportunity to fix one of GAE's misfeatures.  When you create a
# reference in GAE it creates a backreference in the referenced
# class. It's this kind of thing that is exactly what I hate about
# Rails. It represents bad code in so many ways:
#
# * The name of the reference is not in the class that gets it which
#   violates the principal of structural locality. If we defined all
#   objects like this it would be a mess.
# * It's added wether you use it or not.  If we could refactor these
#   out, we would.  But we can't.  Unused code is a liability.
# * Auto-generated names can conflict - meaning you have to deal with
#   these reverse references even if you don't want them and you never
#   use them.
#
# GAE's model system is very much based on Django's but Google left
# out an important Django feature.  The equivalent of
# ReferenceProperties in Django can have string class specifiers.
# This is huge because Python can't deal with circular imports and
# thus circular references are impossible to implement.  We accomplish
# this by resolving the reference class later and look up the
# reference class as needed.
class ReferenceProperty(db.ReferenceProperty):

  def __init__(self,
               reference_class=None,
               verbose_name=None,
               **attrs):
    super(db.ReferenceProperty, self).__init__(verbose_name, **attrs)

    if reference_class is None:
      reference_class = Model

    self.reference_class = reference_class

  def __property_config__(self, model_class, property_name):
    super(db.ReferenceProperty, self).__property_config__(model_class,
                                                          property_name)

    if self.reference_class is db._SELF_REFERENCE:
      self.reference_class = model_class

  def validate(self, value):
    if isinstance(value, datastore.Key):
      return value

    if value is not None and not value.has_key():
      raise BadValueError(
          '%s instance must have a complete key before it can be stored as a '
          'reference' % self.reference_class.kind())

    value = super(db.ReferenceProperty, self).validate(value)

    if isinstance(self.reference_class, basestring):
        if self.reference_class in db._kind_map:
            self.reference_class = db._kind_map[self.reference_class]
        else:
            raise KindError('Property has undefined class type %s' %
                            (self.reference_class))

    if not ((isinstance(self.reference_class, type) and
             issubclass(self.reference_class, Model)) or
            self.reference_class is db._SELF_REFERENCE):
        raise KindError('reference_class must be Model or _SELF_REFERENCE')

    if value is not None and not isinstance(value, self.reference_class):
      raise KindError('Property %s must be an instance of %s' %
                            ("", self.reference_class.kind()))

    return value

  def as_json(self, model_instance, value=None):
    if value is None:
      value = self.get_value_for_datastore(model_instance)
    return str(value)

### ReverseReferenceProperty

# Although I hate autogenerated reverse references, reverse references
# themselves are pretty useful and so we make this class public and
# add support for string reference class specifiers.
#
# Note that we derive ReverseReferenceProperty from object to avoid
# being detected as a property. The original code avoids this by
# binding the property later.
class ReverseReferenceProperty(object):
    
  def __init__(self, model, prop):
    self.__model = model
    self.__property = prop

  @property
  def _model(self):
    if isinstance(self.__model, basestring):
      self.__model = db.class_for_kind(self.__model)
    return self.__model

  @property
  def _prop_name(self):
    """Internal helper to access the property name, read-only."""
    return self.__property

  def __get__(self, model_instance, model_class):
    if model_instance is not None:
      query = Query(self._model)
      return query.filter(self.__property + ' =', model_instance.key())
    else:
      return self

  def __property_config__(self, model_class, attr_name):
      pass

### Computed Properties

# We provide a replacement for GAE's `ComputedProperty` that differs
# from the original in a few ways.  First, we have seperated the class
# from the decorator so that the decorator can take arguments.  These
# arguments allow us to set a return type to associate with the
# property.  And second, we have added an `as_json` method that uses
# this type to produce an appropriate representation for the JSON
# encoder.
class ComputedProperty(db.Property):

  def __init__(self, value_function, kind, name, indexed=True):
      super(ComputedProperty, self).__init__(indexed=indexed)
      self.__value_function = value_function
      self._kind = kind
      self._name = name

  def __set__(self, *args):
      raise db.DerivedPropertyError(
          'Computed property %s cannot be set.' % self.name)

  def __get__(self, model_instance, model_class):
      if model_instance is None:
          return self
      return self.__value_function(model_instance)

  def as_json(self, model_instance):
      value = self.__get__(model_instance, None)
      return self._kind.as_json(model_instance, value=value)

# We use a decorator class to return a `ComputedProperty`.  Python's
# documentation on how this sort of thing works is a bit weak but
# Bruce Eckel has put together a nice [decorator tutorial][eckel] that
# demonstrates advanced decorator usage.
# [eckel]: http://www.artima.com/weblogs/viewpost.jsp?thread=240845 "Python Decorators II: Decorator Arguments"
class computed_property(object):

  def __init__(self, kind, indexed=True):
    self.kind = kind
    self.indexed = indexed

  def __call__(self, f, *args):
    return ComputedProperty(f, *args, kind=self.kind, name=f.func_name, indexed=self.indexed)

### Models

# Ideally I'd like Models to be drop in replacement in the same way
# that types are but GAE keeps a map of model names and also does a
# several special checks such that db.Model acts differently than its
# subclasses. Building pluggable replacements is therefore difficult.
# Instead, we let Model be db.Model and then we define our own variants.
Model = db.Model

# Our model variations have a lot of shared functionality that we push
# into a mixin.
class ModelMixin(object):

    def _json_dumps(self, obj):
        return json.dumps(obj)

    def _to_json(self, options={}, include=None, exclude=None):
        return json.dumps(self.as_json(options=options, include=include, exclude=exclude))

    def to_json(self, options={}, include=None, exclude=None):
        return self._to_json(options, include, exclude)

    # Most of the clever stuff happens here.  We iterate through the
    # properties checking them against the properties we should expose
    # (via `include` and `exclude`).  We then call the individual
    # properties' `as_json` methods to build the final representation.
    def _as_json(self, options={}, include=None, exclude=None):
        result = {}
        available_properties = self.properties()
        if include:
            properties = include
        else:
            properties = self.properties().keys()
            if exclude:
                for x in exclude:
                    properties.remove(x)
        for p in properties:
            if p[0:1] == "_":
                continue
            if p in available_properties:
                p_kind = self.properties()[p]
                try:
                    result[p] = p_kind.as_json(self)
                except:
                    result[p] = None
        return result

    # Since overriding `as_json` is pretty common and calling super
    # class methods is a pain in Python, we put the core behavior in
    # `_as_json`.
    def as_json(self, options={}, include=None, exclude=None):
        return self._as_json(options, include, exclude)

    # Likewise we can extract a representation from json. TODO.
    def _from_json(self, data, options={}, include=None, exclude=None):
        available_properties = self.properties()
        if include:
            properties = include
        else:
            properties = self.properties().keys()
            if exclude:
                for x in exclude:
                    properties.remove(x)
        for p in properties:
            if p in available_properties:
                if p in data:
                    setattr(self, p, data[p])
        self.put()

    def from_json(self, data, options={}, include=None, exclude=None):
        return self._from_json(data, options, include, exclude)

### MoraModel
# We use our mixin to define Mora's base model.
class MoraModel(db.Model, ModelMixin):

    @computed_property(StringProperty(default=""))
    def id(self):
        if self.is_saved():
            return str(self.key())
        return ""

    # We also add the method class_name to our base model to mirror
    # the class_name method in Google's PolyModel class.
    @classmethod
    def class_name(cls):
        return cls.kind()

### MoraPolyModel
# And we also use our mixin to define Mora's base polymodel.
class MoraPolyModel(polymodel.PolyModel, ModelMixin):

    @computed_property(StringProperty(default=""))
    def id(self):
        if self.is_saved():
            return str(self.key())
        return ""


def create(model):
    _class = db.class_for_kind(model)
    return _class()

