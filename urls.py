from django.conf.urls.defaults import *
from edu.nau.zabeta.dispatch import dispatch_api

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'index.html'}),
    (r'^api/(?P<method>.*)$', dispatch_api),
)
