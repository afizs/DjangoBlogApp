from django.conf.urls import url
from . import views


app_name = 'posts'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<post_id>\d+)/$', views.detail, name="detail"),
    url(r'^(?P<post_id>\d+)/update/$', views.update, name='update'),
    url(r'^(?P<post_id>\d+)/delete/$', views.delete, name='delete'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', views.login, name='login'),


]
