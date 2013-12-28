from django.conf.urls import patterns, include, url
from django.contrib import admin
from freepl.views import init,mainpage,loginit,logoutit,registerit
from freepl.views import locktheteamit,user_verify
admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$',init),
   url(r'^dummylogin$', loginit),
   url(r'^dummyregister$', registerit),
   url(r'^dummylocktheteam$', locktheteamit),
   url(r'^dummylogout$', logoutit),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^qwe/', mainpage),
   url(r'^activate/(?P<activation_key>\w+)/$', user_verify),

)
