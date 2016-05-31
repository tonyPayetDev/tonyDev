# -*- coding: utf-8 -*-
"""
Author: Philippe 'paHpa' Vivien <philippe.vivien@nerim.com>

Copyright: Nerim, 2015
"""
from __future__ import unicode_literals

from django.http import Http404

from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer



from blacklist.models import Blacklist



from .serializers import  JuridictionSerializer 
from .permissions import IsAdminOrReadOnly
from .mixins import PutUpdateModelMixin

from runner.utils.logger import logger
from runner.utils.jsonresponse import JSONResponse
from runner.utils.choices import BIZ_LIST, ZONE_LIST, PHONEKIND_LIST
from runner.utils.dataset import format_datatable , formatdataT
from django.contrib.auth.models import User

tab=[]

class CustomPagination(PageNumberPagination):
    """
    Default pagination class.
    Let large result sets be split into individual pages of data.
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100000


class BaseViewSet2(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    filter_backends = (filters.SearchFilter,)
#    pagination_class = CustomPagination
#    paginate_by = 100
     
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)


class CustomPagination2(PageNumberPagination):
#    page_size = 10
#    page_size_query_param = 'page_size'
#    max_page_size = 1000
    paginate_by = None
    
class JuridictionViewSet(BaseViewSet2):

    queryset = Blacklist.objects.all()
    search_fields = ('id','email')
    serializer_class = JuridictionSerializer
    pagination_class = CustomPagination
    

    def get(self, request, pk, format=None):
        logger.debug("request = %s pk = %s"%(request, pk))
        juri = self.get_object(pk) 
        serializer = JuridictionSerializer(juri)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):

        juridiction = self.get_object()
        print "juridiction"
        print
        blacklist=Blacklist.objects.get(pk=pk)
        
        serializer = JuridictionSerializer(blacklist,data={"user":4,"email":request.data['data[email]'],"type_blacklist":request.data['data[type_blacklist]']})
        print serializer.is_valid()
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
          
    def post(self, request, pk ,format=None):
        user=User.objects.get(username=self.request.user) 
        print user
        data={"user":user.id,"email":request.data['data[email]'],"type_blacklist":request.data['data[type_blacklist]']}
        serializer = JuridictionSerializer(data=data)
        print serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):

	test=request.data
	myDict = {}
	for key in test.iterkeys():
	    myDict[key] = test.getlist(key)
		
	for pk in myDict['id[]']:
		juri = Blacklist(pk=pk)  
		juri.delete()

        return Response({"aaData": []})


 

