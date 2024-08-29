from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from college.models import *
from college.serializers import *



class CollegeListViewset(GenericViewSet):
    def get(self,request):
        try:
            college = College.objects.all()
            serializer = CollegeSerializer(college,many=True)
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

            


