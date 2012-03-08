import datamodel
import urllib
import session

from google.appengine.ext import blobstore,webapp,db
from google.appengine.ext.webapp import blobstore_handlers

class test(session.session):

    def get(self):
        upload_url = blobstore.create_upload_url('/file/upload/'+self.user['id'])
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit" name="submit" value="Submit"> </form></body></html>""")

        for b in blobstore.BlobInfo.all():
            self.response.out.write('<li><a href="/file/download/%s' % str(b.key()) + '">' + str(b.filename) + '</a>')

class UploadFile(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):
        sess=session.session(self.request,self.response)
        id=self.request.path.split("/")[-1]
        model=db.get(id)      
        collection=model.class_name()
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        key=str(blob_info._BlobInfo__key)          
        if collection == "University":
            model.thumbnail=key
            model.save()
        elif collection == "Program":
            model.thumbnail=key
            model.save()
        elif collection == "CourseOffering":
            model.syllabus=key
            model.save()
        elif collection == "Minutes":
            model.attachment.append(key)
            model.save()
        elif collection == "User":
            model.thumbnail=key
            model.save()
            sess.user['thumbnail']=key
            sess.save_session()
                      
        #todo remove,  debug only
        self.redirect("/file/%d/success" % (blob_info.key().id(),))


class AjaxSuccessHandler(session.session):
  def get(self, file_id):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('%s/file/%s' % (self.request.host_url, file_id))


class DownloadFile(blobstore_handlers.BlobstoreDownloadHandler):

    def get(self, blob_key):
        #This will exit if the user isn't authenticated. 
        session.session(self.request,self.response)
        blob_key = str(urllib.unquote(blob_key))
        if not blobstore.get(blob_key):
            self.error(404)
        else:
            self.send_blob(blobstore.BlobInfo.get(blob_key), save_as=True)
