from django.conf.urls import url

from thornhillsystem import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^email_sender/$', views.email_sender, name='email_sender'),
    url(r'^temperature/$', views.temperature, name='temperature'),
]
