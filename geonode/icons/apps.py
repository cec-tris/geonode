from django.apps import AppConfig
from django.conf.urls import url, include
from django.conf import settings

class IconsConfig(AppConfig):
    name = 'geonode.icons'
    default_auto_field = 'django.db.models.BigAutoField'
    def ready(self):
        from geonode.urls import urlpatterns

        urlpatterns += [url(r"^icons/", include("geonode.icons.urls"))]



    