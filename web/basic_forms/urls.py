from django.conf.urls import patterns, url

from basic_forms import views

mv = views.MainView()

urlpatterns = patterns('', url(r'^$', mv.index, name='index'),)
