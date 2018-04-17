from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create/character$', views.create_char, name="create_char"),
    url(r'^submit/character$', views.submit_char, name="submit_char"),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^submit$', views.submit),
    url(r'^battle/(?P<floor>\d+)/(?P<room>\d+)$', views.battle, name="battle"),
    url(r'^dungeon/(?P<floor>\d+)/(?P<room>\d+)$', views.dungeon, name="dungeon")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)