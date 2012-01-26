'''
Created on Jan 26, 2012

@author: Jonah Hirsch
'''
import api

class getdepartments(api.api):

    def run(self, request, extra_context=None, mimetype=None, **kwargs):
        self.output=["Computer Science","Engineering","Whatever"]