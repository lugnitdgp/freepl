from django.conf.urls import patterns, include, url
from django.contrib import admin
from freepl.views import home,authorize,logout_
from freepl.views import locktheteam
from mysite import settings
admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$',home),
   url(r'^authorize/',authorize),
   url(r'^dummylocktheteam$', locktheteam),
   url(r'^dummylogout$', logout_),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),

)
