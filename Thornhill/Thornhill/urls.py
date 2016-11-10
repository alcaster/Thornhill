from django.conf.urls import url
from django.contrib import admin
from thornhillsystem import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^email_sender/$', views.email_sender, name='email_sender'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
