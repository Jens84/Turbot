from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Turbot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('basic_forms.urls', namespace="basic_forms")),
    url(r'^admin/', include(admin.site.urls)),
)
