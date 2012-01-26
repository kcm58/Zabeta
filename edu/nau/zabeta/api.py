'''
Created on Jan 26, 2012

@author: Jonah Hirsch
'''
from django.template import loader, RequestContext
from django.http import HttpResponse
import json

def get_json(request, template, extra_context=None, mimetype=None, **kwargs):
    if extra_context is None: extra_context = {}
    struct = {'message': 'Hello!', '3': [1,2,3]}
    json_obj = json.dumps(struct)
    dictionary = {'json': json_obj}
#    for key, value in extra_context.items():
#        if callable(value):
#            dictionary[key] = value()
#        else:
#            dictionary[key] = value
    c = RequestContext(request, dictionary)
    t = loader.get_template(template)
    return HttpResponse(t.render(c), mimetype='application/json')