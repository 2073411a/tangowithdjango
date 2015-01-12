from django.comf.urls import patterns,url
from randgo import views
urlpatterns = patterns('',url(r'^$'.views.index,name='index'))
