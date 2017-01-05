from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as rest_views

from thornhillsystemrestapi import views

router = routers.DefaultRouter()
router.register(r'mails', views.MailViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', rest_views.obtain_auth_token),
]
