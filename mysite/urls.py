from django.conf.urls import patterns, include, url
from django.contrib import admin
from freepl.views import home,login_,logout_,register
from freepl.views import locktheteam,user_verify
admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$',home),
   url(r'^dummylogin$', login_),
   url(r'^dummyregister$', register),
   url(r'^dummylocktheteam$', locktheteam),
   url(r'^dummylogout$', logout_),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^activate/(?P<activation_key>\w+)/$', user_verify),

)
