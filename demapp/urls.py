from django.conf.urls import url

from demapp import views

urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'^gitIssues/$', views.gitIssues, name='gitIssues'),

]
