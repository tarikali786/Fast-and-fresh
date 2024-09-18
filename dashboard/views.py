from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from college.models import *
from college.serializers import *
from dashboard.serializers import *


class CollegeListViewset(GenericViewSet):

    def create(self, request):
        serializer = CollegeDashboardSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
                
        




    def list(self,request):
        try:
            college = College.objects.all()
            serializer = CollegeSerializer(college,many=True)
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

            

    def get(self,request,uid):
        try:
            college = College.objects.get(uid=uid)

        except College.DoesNotExist:
            return Response({"error":"College not found"},status=status.HTTP_404_NOT_FOUND)

        try:
            campusList = Campus.objects.filter(college=college)

        except Campus.DoesNotExist:
            return Response({"error":"Campus not found"},status=status.HTTP_404_NOT_FOUND)

        college_serializer = CollegeDetailsSerializer(college)
        campus_serializer = CampusDashboardSerializer(campusList,many=True)

            
        return Response({"data":college_serializer.data,"campus_data":campus_serializer.data},status=status.HTTP_200_OK)
       
 

class CampusDetailsViewset(GenericViewSet):
    def get(self,request,uid):
        try:
            campus = Campus.objects.get(uid=uid)
        except Campus.DoesNotExist:
            return Response({"error":"Campus not found"},status=status.HTTP_404_NOT_FOUND)
        
        try:
            studentList = Student.objects.filter(campus= campus)
        except Student.DoesNotExist:
            return Response({"error":"Student not found"},status=status.HTTP_404_NOT_FOUND) 
        try:
            faculty_list = Faculty.objects.filter(campus =campus)
        except Faculty.DoesNotExist:
            return Response({"error":"Faculty not found"},status=status.HTTP_404_NOT_FOUND)
        
        campus_serializer = CampusSerializer(campus)
        student_serializer = StudentSerializer(studentList,many=True)
        faculty_serializer = facultyDashboardSerializer(faculty_list,many=True)
        return Response({"data":campus_serializer.data,"student_list":student_serializer.data,"faculty_list":faculty_serializer.data},status=status.HTTP_200_OK)
        


class EmployeeDetailsViewset(GenericViewSet):

    def get(self,request,uid):
        try:
            employee = Employee.objects.get(uid=uid)
            serializers = EmployeeDashboardSerializer(employee)
            return Response({"data":serializers.data},status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"error":"Employee not found"},status=status.HTTP_404_NOT_FOUND)



class CollectionListViewSet(GenericViewSet):
    def list(self,request):
        try:
            collectionList = Collection.objects.all()
            serializer = CollectionDashboardSerializer(collectionList,many=True)
            return Response (serializer.data,status=status.HTTP_200_OK)
        except Collection.DoesNotExist:
            return Response({"error":"Collection not found"},status=status.HTTP_404_NOT_FOUND)
        
        