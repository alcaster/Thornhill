from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from thornhillsystem import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^email_sender/$', views.email_sender, name='email_sender'),
]
