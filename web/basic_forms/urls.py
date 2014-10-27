from django.conf.urls import patterns, url

from basic_forms import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
