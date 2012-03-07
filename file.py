import datamodel
import urllib

from google.appengine.ext import blobstore,webapp,db
from google.appengine.ext.webapp import blobstore_handlers

class test(webapp.RequestHandler):

    def get(self):
        upload_url = blobstore.create_upload_url('/file/upload/agxkZXZ-emFiZXRhLTJyCwsSBFVzZXIYjAIM')
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit" name="submit" value="Submit"> </form></body></html>""")

        for b in blobstore.BlobInfo.all():
            self.response.out.write('<li><a href="/serve/%s' % str(b.key()) + '">' + str(b.filename) + '</a>')

class UploadFile(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):
        id=self.request.path.split("/")[-1]
        model=db.get(id)      
        collection=model.class_name()
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        key=blob_info._BlobInfo__key          
        if collection == "University":
            datamodel.University.thumbnail=key
            datamodel.University.save()
        elif collection == "Program":
            datamodel.Program.thumbnail=key
            datamodel.Program.save()
        elif collection == "CourseOffering":
            datamodel.CourseOffering.syllabus=key
            datamodel.CourseOffering.save()
        elif collection == "Minutes":
            datamodel.Minutes.attachment=key
            datamodel.Minutes.save()
        elif collection == "User":
            datamodel.User.thumbnail=key
            datamodel.User.save()            
        #todo remove,  debug only
        self.redirect('/file/test')

class DownloadFile(blobstore_handlers.BlobstoreDownloadHandler):

    def get(self, blob_key):
        blob_key = str(urllib.unquote(blob_key))
        if not blobstore.get(blob_key):
            self.error(404)
        else:
            self.send_blob(blobstore.BlobInfo.get(blob_key), save_as=True)
