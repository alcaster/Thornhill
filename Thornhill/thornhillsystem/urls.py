from django.conf.urls import url
from thornhillsystem import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]