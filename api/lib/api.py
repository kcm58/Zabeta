'''
Created on Jan 26, 2012

@author: Jonah Hirsch
'''

class api:
    def __init__(self, test, test2):
        self.output=""
        
    def run(self, request, extra_context=None, mimetype=None, **kwargs):
        pass
    
    def getOutput(self):
        return self.output
        
