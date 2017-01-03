from django.conf.urls import url

from thornhillsystemrestapi import views

urlpatterns = [
    url(r'^', views.test),
]
