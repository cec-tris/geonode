from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"data/(?P<dataid>\w+)$", views.getdata, name="getdata"),
    url(r"search/geocode$", views.geocode, name="geocode"),
    url(r"search/reversegeocode$", views.reversegeocode, name="reversegeocode"),
]