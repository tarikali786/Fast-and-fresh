from rest_framework.response import Response
from django.db.models.functions import TruncMonth,Cast
from django.db.models import Count
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from college.models import *
from college.serializers import *
from dashboard.serializers import *
from django.db.models import FloatField, Sum

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
        
    

class RouteListDashboardViewset(GenericViewSet):
    def list(self,request):
        try:
            routeList = Routes.objects.all()
            serializer = RouteDashboardSerializer(routeList,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Routes.DoesNotExist:
            return Response({"error":"Route not found"},status=status.HTTP_404_NOT_FOUND)
        


class AnalyticViewset(GenericViewSet):
    def list(self,request):
        monthly_college_data = College.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
        college_data = list(monthly_college_data)

        monthly_Student_data = Student.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
        student_data = list(monthly_Student_data)

        monthly_campus_data = Campus.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
        campus_data = list(monthly_campus_data)

        monthly_Collection_data = Collection.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
        collection_data = list(monthly_Collection_data)

        total_earnings = College.objects.annotate(monthly_payment_float=Cast('monthly_payment', FloatField()))\
                            .aggregate(total_earnings_sum=Sum('monthly_payment_float'))
        
        monthly_earnings = College.objects.annotate(month=TruncMonth('created_at'))\
                            .annotate(monthly_payment_float=Cast('monthly_payment', FloatField()))\
                            .values('month')\
                            .annotate(count=Sum('monthly_payment_float'))\
                            .order_by('month')
        
        total_colleges = College.objects.count()
        total_campus = Campus.objects.count()
        total_student = Student.objects.count()
        total_Employee = Employee.objects.count()
        total_Vehcile = Vehicle.objects.count()



        return Response({
            "college":college_data,
            "total_colleges":total_colleges,
            "student":student_data,
            "total_student":total_student,
            "campus":campus_data,
            "total_campus":total_campus,
            "collection":collection_data,
            "total_earnings":total_earnings['total_earnings_sum'] ,
            "monthly_earnings":list(monthly_earnings),
            "total_Vehcile":total_Vehcile,
            "total_Employee":total_Employee,

        },status=status.HTTP_200_OK)