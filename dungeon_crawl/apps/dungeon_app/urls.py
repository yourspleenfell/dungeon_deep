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
    url(r'^treasure/(?P<floor>\d+)/(?P<room>\d+)$', views.treasure, name="treasure"),
    url(r'^dungeon/(?P<floor>\d+)/(?P<room>\d+)$', views.dungeon, name="dungeon"),
    url(r'^random/(?P<floor>\d+)/(?P<room>\d+)$', views.random_gen, name="random"),
    url(r'^progress/(?P<floor>\d+)/(?P<room>\d+)$', views.progress, name="progress"),
    url(r'^shop$', views.shop),
    url(r'^upload$', views.model_form_upload, name="upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)