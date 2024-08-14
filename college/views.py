from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
# Create your views here.


# class College()

class TestApi(GenericViewSet):
    def get(self,request):
        return Response({"Message":"Backend connect successfully"})