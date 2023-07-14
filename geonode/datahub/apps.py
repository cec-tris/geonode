from django.apps import AppConfig
from django.conf import settings
from django.conf.urls import url, include


class DataHubConfig(AppConfig):
    name = 'geonode.datahub'
    default_auto_field = 'django.db.models.BigAutoField'
    def ready(self):
        from geonode.urls import urlpatterns
        urlpatterns += [url(r"^datahub/", include("geonode.datahub.urls"))]
