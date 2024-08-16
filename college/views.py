from rest_framework import viewsets, status
from rest_framework.response import Response
from college.models import Employee, College,Campus,Faculty,Student
from .serializers import (EmployeeSerializer, EmployeeDailyImageSerializer, 
                          CollegeSerializer, CampusSerializer,
                          FacultySerializer,StudentSerializer,
                          )


class EmployeeViewSet(viewsets.GenericViewSet):
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            
            # Handle the uploaded daily images
            daily_images_files = request.FILES.getlist('daily_images')
            for image_file in daily_images_files:
                image_serializer = EmployeeDailyImageSerializer(data={'image': image_file})
                if image_serializer.is_valid():
                    daily_image_instance = image_serializer.save()
                    employee.daily_images.add(daily_image_instance)
            
            return Response({"message": "Employee created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        





# crud operation for College model
class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    lookup_field = 'uid'


# Curd operation for Campus Model
class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    lookup_field = 'uid'


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    lookup_field = 'uid'


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'uid'