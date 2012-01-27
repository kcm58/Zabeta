'''
Created on Jan 26, 2012

@author: Jonah Hirsch
'''
import json
from django.template import loader, RequestContext
from django.http import HttpResponse
import api.getdepartments

def dispatch_api(request, extra_context=None, mimetype=None, **kwargs):
    if extra_context is None: extra_context = {}
    
    method = kwargs['method']
#    module = __import__('api.api')
#    class_ = getattr(module, method)
    mod = __import__('api.api')
    c=getattr(mod,method)
    instance = c()
    instance.run(request, extra_context, mimetype, **kwargs)
    
    json_obj = json.dumps(instance.getOutput())
    dictionary = {'json': json_obj}

    c = RequestContext(request, dictionary)
    t = loader.get_template("json.html")
    return HttpResponse(t.render(c), mimetype='application/json')