'''
Created on Jan 26, 2012

@author: Jonah Hirsch
'''

class api:
    public={}
    def __init__(self,request):
        self.request=request
        self.output=""
    
    def getOutput(self):
        return self.output
      
    def getPublic(self):
        return self.public
