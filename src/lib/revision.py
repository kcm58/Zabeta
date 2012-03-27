from mora.rest import RestHandler,rest_create
from mora import db
import datamodel
import datetime

#Everything below here is revisioned
class revision(RestHandler):
     
    def duplicate(self,src,dest):
        #iterate over each parameter specified in the select
        for key in src._all_properties:
            if key!="id":
                val=getattr(src,"_"+key)
                setattr(dest,key,val)    
#            t=type(var)
#            if t is list:
#                if len(var) and type(var[0]) is db.Key:
#                    ids=[]
#                    for v in var:
#                        ids.append(str(v))
#                    element[key]=ids
#            else:
#                element[key]=str(var)
#        return element

    def version_save(self,new_ver):
        name=new_ver.class_name()
        collection=getattr(datamodel,name) 
        
        v=collection()
        self.duplicate(new_ver,v)
        v.commit_user=self.user['id']
        v.commit_program=self.program_id
        v.commit_university=self.university_id
        #This is a new minor revision
        v.commit_minor+=1
        v.commit_timestamp=datetime.datetime.now()
        v.save()
