from json import dumps
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core import serializers

from rest_framework import routers, serializers, viewsets, generics, pagination
from django.db.models import Q

from .models import Icon
from .forms import IconForm

class IconSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Icon
        fields = ['name', 'path']

class ExamplePagination(pagination.PageNumberPagination):       
       page_size = 2
       page_size_query_param= "limit"

class IconViewSet(viewsets.ModelViewSet):
    queryset = Icon.objects.all()
    serializer_class = IconSerializer
    pagination_class=ExamplePagination
    def get_queryset(self):
        """
        Optionally restricts the returned articles to given regions,
        by filtering against a `regions` query parameter in the URL.
        """
        textSearch = self.request.query_params.get("search", None)
        user = self.request.user
        if(textSearch is None):
            return super().get_queryset()
        
        # if (name := self.kwargs.get("name", None) is not None):
        #     qs =  Author.objects.filter(
        #         Q(first_name__icontains=name)
        #         | Q(last_name__icontains=name)
        #         | Q(user__name__icontains=name)
        #         | Q(user__username__icontains=name)
        #     )
        qs = Icon.objects.filter()
        qs = qs.filter(name__icontains=textSearch)

        return qs
    
def index(request):
    return HttpResponse("Icons")


