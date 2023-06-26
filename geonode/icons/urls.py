from django.urls import path, include
from rest_framework import routers
from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'', views.IconViewSet)

urlpatterns = [
    path(
        "", views.IconViewSet.as_view(actions={"get": "list"}), name="icons_list"
    ),
    path('index', views.index, name='index'),
]