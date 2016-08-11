from django.conf.urls import include, url
#from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include('admin.urls', namespace="admin")),
    #url(r'^admin/', include(admin.site.urls)),
]