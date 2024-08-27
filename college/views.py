from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
import json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from college.models import (Employee, College,Campus,Faculty,Student,
                            WashingMashine, DryingMashine,Vehicle, VehicleExpenses,FoldingTable,
                            complaint,Collection,StudentDaySheet,FacultyDaySheet,StudentRemark,
                            RemarkByWarehouse,Routes
                            )
from .serializers import (EmployeeSerializer, EmployeeDailyImageSerializer, 
                          CollegeSerializer, CampusSerializer,
                          FacultySerializer,StudentSerializer,
                          WashingMashineSerializer,WashingMashineCleanImageSerializer,
                          DryingMashineSerializer,VehicleSerializer,VehicleExpensesSerializer,
                          FoldingTableSerializer,complaintSerializer,CollectionSerializer,
                          DailyImageSheetSerializer,StudentDaySheetSerializer,FacultyDaySheetSerializer,
                          StudentRemarkSerializer,RemarkByWarehouseSerializer,
                          EmployeeSignInserializer,GetCampusSerializer,RoutesSerializer,CollectionTaskSerializer
                          )


class EmployeeViewSet(viewsets.GenericViewSet):
    def create(self, request):
        email = request.data.get("email")
        if Employee.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            serializer = EmployeeSerializer(data=request.data)
            if serializer.is_valid():
                employee = serializer.save()

                # Handle the uploaded daily images from request.FILES
                daily_images_files = request.FILES.getlist('daily_images')
                for image_file in daily_images_files:
                    image_serializer = EmployeeDailyImageSerializer(data={'image': image_file})
                    if image_serializer.is_valid():
                        daily_image_instance = image_serializer.save()
                        employee.daily_images.add(daily_image_instance)

                return Response({"message": "Employee created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AllEmployeeViewset(viewsets.GenericViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def get(self,request):
        return Response({"message": "All Employees", "data": self.serializer_class(self.queryset,
                                                                                   many=True).data}, status=status.HTTP_200_OK)
    
class EmployeeLogoutViewset(viewsets.GenericViewSet):
    permission_classes =[IsAuthenticated]
    def logout(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    

class EmployeeSignInViewset(viewsets.GenericViewSet):
    def post(self,request):
        serializer = EmployeeSignInserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        employee = Employee.objects.filter(email=email).first()

        if employee:
            # if employee.check_password(password):
            if employee.password == password:    
                refresh = RefreshToken.for_user(employee)
                employee_data= EmployeeSerializer(employee)

                return Response({"data":employee_data.data,"refresh-token": str(refresh), "access-token": str(refresh.access_token)}, status=200)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
            
                                
        else:
            return Response({"error": "Employee not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        



# crud operation for College model
class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    lookup_field = 'uid'



class RoutesViewSet(viewsets.ModelViewSet):
    queryset = Routes.objects.all()
    serializer_class = RoutesSerializer
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
    

class WashingMashineViewSet(viewsets.ModelViewSet):
    queryset = WashingMashine.objects.all()
    serializer_class = WashingMashineSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            washing_mashine = serializer.save()

            before_and_after_cleaned_image_files = request.FILES.getlist('before_and_after_cleaned_image')
            for image_file in before_and_after_cleaned_image_files:
                image_serializer = WashingMashineCleanImageSerializer(data={'image': image_file})
                if image_serializer.is_valid():
                    daily_image_instance = image_serializer.save()
                    washing_mashine.before_and_after_cleaned_image.add(daily_image_instance)
                else:
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "Washing Machine created successfully", "data": serializer.data},
                             status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
    
    def delete(self,request,uid):
        try:
            obj = WashingMashine.objects.get(uid=uid)
            obj.delete()
            return Response({"message": "Washing Machine deleted successfully"}, status=status.HTTP_200_OK)
        except WashingMashine.DoesNotExist:
            return Response({"message": "Washing Machine not found"}, status=status.HTTP_404_NOT_FOUND
                            )
        
    def update(self,request,uid):
        try:
            obj = WashingMashine.objects.get(uid=uid)
            serializer = self.get_serializer(obj, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Washing Machine updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        except WashingMashine.DoesNotExist:
            return Response({"message": "Washing Machine not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def get(self,request,uid):
        try:
            obj = WashingMashine.objects.get(uid=uid)
            serializer = self.get_serializer(obj)
            return Response({"data": serializer.data},status=status.HTTP_200_OK)
        except WashingMashine.DoesNotExist:
            return Response({"message": "Washing Machine not found"}, status=status.HTTP_404_NOT_FOUND)


class DryingMashineViewSet(viewsets.ModelViewSet):
    queryset = DryingMashine.objects.all()
    serializer_class = DryingMashineSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            washing_mashine = serializer.save()

            # Handle the before_and_after_cleaned_image files
            before_and_after_cleaned_image_files = request.FILES.getlist('before_and_after_cleaned_image')
            for image_file in before_and_after_cleaned_image_files:
                image_serializer = WashingMashineCleanImageSerializer(data={'image': image_file})
                if image_serializer.is_valid():
                    daily_image_instance = image_serializer.save()
                    washing_mashine.before_and_after_cleaned_image.add(daily_image_instance)
                else:
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "Drying Machine created successfully", "data": serializer.data},
                             status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
    

    def delete(self,request,uid):
        try:
            obj = DryingMashine.objects.get(uid=uid)
            obj.delete()
            return Response({"message": "Drying Machine deleted successfully"}, status=status.HTTP_200_OK)
        except DryingMashine.DoesNotExist:
            return Response({"message": "Drying Machine not found"}, status=status.HTTP_404_NOT_FOUND
                            )
        
    def update(self,request,uid):
        try:
            obj = DryingMashine.objects.get(uid=uid)
            serializer = self.get_serializer(obj, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Drying Machine updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        except DryingMashine.DoesNotExist:
            return Response({"message": "Drying Machine not found"}, status=status.HTTP_404_NOT_FOUND)

    
    def get(self,request,uid):
        try:
            obj = DryingMashine.objects.get(uid=uid)
            serializer = self.get_serializer(obj)
            return Response({"data": serializer.data},status=status.HTTP_200_OK)
        except DryingMashine.DoesNotExist:
            return Response({"message": "Drying Machine not found"}, status=status.HTTP_404_NOT_FOUND)
                            
class VehicleExpensesViewSet(viewsets.ModelViewSet):
    queryset = VehicleExpenses.objects.all()
    serializer_class = VehicleExpensesSerializer
    lookup_field = 'uid'

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    lookup_field = 'uid'    



class FoldingTableViewSet(viewsets.ModelViewSet):
    queryset = FoldingTable.objects.all()
    serializer_class = FoldingTableSerializer
    lookup_field = 'uid'   



class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = complaint.objects.all()
    serializer_class = complaintSerializer
    lookup_field = 'uid' 



class StudentDaySheetViewset(viewsets.ModelViewSet):
    queryset = StudentDaySheet.objects.all()
    serializer_class = StudentDaySheetSerializer
    lookup_field = 'uid' 
   

class FacultyDaySheetViewset(viewsets.ModelViewSet):
    queryset = FacultyDaySheet.objects.all()
    serializer_class = FacultyDaySheetSerializer
    lookup_field = 'uid' 
    

class StudentRemarkViewset(viewsets.ModelViewSet):
    queryset = StudentRemark.objects.all()
    serializer_class = StudentRemarkSerializer
    lookup_field = 'uid' 

class RemarkByWarehouseViewset(viewsets.ModelViewSet):
    queryset = RemarkByWarehouse.objects.all()
    serializer_class = RemarkByWarehouseSerializer
    lookup_field = 'uid' 
class CollectionViewSet(viewsets.GenericViewSet):
    
    def create(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            collection_instance = serializer.save()

            campus_uid = request.data.get('campus_uid')
            supervisor_uid = request.data.get('supervisor_uid')


            drying_supervisor_uid = request.data.get('drying_supervisor_uid',[])
            segregation_supervisor_uid = request.data.get('segregation_supervisor_uid',[])
            drop_driver_uid = request.data.get('drop_driver_uid',[])
            college_supervisor_uid = request.data.get('college_supervisor_uid',[])

           
            try:
                campus_instance = Campus.objects.get(uid=campus_uid)
                collection_instance.campus = campus_instance
                college_instance = College.objects.get(uid=campus_instance.college.uid)
                routes_instance = Routes.objects.get(uid = college_instance.routes.uid)
                if routes_instance:
                    collection_instance.pickup_driver = routes_instance.employee



            except Campus.DoesNotExist:
                return Response({'error': 'Campus not found'}, status=status.HTTP_404_NOT_FOUND)

            try:
                supervisor_instance = Employee.objects.get(uid=supervisor_uid)
                collection_instance.supervisor = supervisor_instance
            except Employee.DoesNotExist:
                return Response({'error': 'Supervisor not found'}, status=status.HTTP_404_NOT_FOUND)
                # Handle optional Employee-related fields
          
            if drying_supervisor_uid:
                try:
                    drying_supervisor_instance = Employee.objects.get(uid=drying_supervisor_uid)
                    collection_instance.drying_supervisor = drying_supervisor_instance
                except Employee.DoesNotExist:
                    return Response({'error': 'Drying supervisor not found'}, status=status.HTTP_404_NOT_FOUND)

            if segregation_supervisor_uid:
                try:
                    segregation_supervisor_instance = Employee.objects.get(uid=segregation_supervisor_uid)
                    collection_instance.segregation_supervisor = segregation_supervisor_instance
                except Employee.DoesNotExist:
                    return Response({'error': 'Segregation supervisor not found'}, status=status.HTTP_404_NOT_FOUND)

            if drop_driver_uid:
                try:
                    drop_driver_instance = Employee.objects.get(uid=drop_driver_uid)
                    collection_instance.drop_driver = drop_driver_instance
                except Employee.DoesNotExist:
                    return Response({'error': 'Drop driver not found'}, status=status.HTTP_404_NOT_FOUND)

            if college_supervisor_uid:
                try:
                    college_supervisor_instance = Employee.objects.get(uid=college_supervisor_uid)
                    collection_instance.college_supervisor = college_supervisor_instance
                except Employee.DoesNotExist:
                    return Response({'error': 'College supervisor not found'}, status=status.HTTP_404_NOT_FOUND)

            # Update the ETA based on the college's schedule
            collection_instance.ETA = college_instance.schedule

            collection_instance.save()
            
            # Save nested related objects
            student_day_sheet= json.loads(request.data.get('student_day_sheet', '[]'))
            for student_day in student_day_sheet:
                student_day_sheet_serializer = StudentDaySheetSerializer(data=student_day)
                if student_day_sheet_serializer.is_valid():
                    student_day_sheet_instance = student_day_sheet_serializer.save()
                    collection_instance.student_day_sheet.add(student_day_sheet_instance)


            faculty_day_sheet = json.loads(request.data.get('faculty_day_sheet', '[]'))
            for faculty_day in faculty_day_sheet:
                faculty_day_sheet_serializer = FacultyDaySheetSerializer(data=faculty_day)
                if faculty_day_sheet_serializer.is_valid():
                    faculty_day_sheet_instance = faculty_day_sheet_serializer.save()
                    collection_instance.faculty_day_sheet.add(faculty_day_sheet_instance)


            student_remark_list  = json.loads(request.data.get('student_remark', '[]'))
            if student_remark_list is not None:
                for student_remark in student_remark_list:
                    student_remark_serializer = FacultyDaySheetSerializer(data=student_remark)
                    if student_remark_serializer.is_valid():
                        student_remark_instance = student_remark_serializer.save()
                        collection_instance.student_remark.add(student_remark_instance)

            warehouse_remark_list  = json.loads(request.data.get('student_remark', '[]'))
            if student_remark_list is not None:
                for warehouse_remark in warehouse_remark_list:
                    warehouse_remark_serializer = FacultyDaySheetSerializer(data=warehouse_remark)
                    if warehouse_remark_serializer.is_valid():
                        warehouse_remark_instance = warehouse_remark_serializer.save()
                        collection_instance.warehouse.add(warehouse_remark_instance)
            
            # Handle the uploaded daily images from request.FILES
            daily_image_sheet_file = request.FILES.getlist('daily_image_sheet')
            for image_file in daily_image_sheet_file:
                image_serializer = DailyImageSheetSerializer(data={'image': image_file})
                if image_serializer.is_valid():
                    daily_image_instance = image_serializer.save()
                    collection_instance.daily_image_sheet.add(daily_image_instance)
            
            collection_instance.save()
            
            collection_serializer = CollectionSerializer(collection_instance)
            return Response({"message": "Collection created successfully", "data": collection_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)



    def update(self, request, uid=None):

        try:
            collection_instance = Collection.objects.get(uid=uid)
        except Collection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionSerializer(collection_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            collection_instance = serializer.save()
            
            campus_uid = request.data.get('campus_uid')
            supervisor_uid = request.data.get('supervisor_uid')

            # Optional fields update
            drying_supervisor_uid = request.data.get('drying_supervisor_uid')
            segregation_supervisor_uid = request.data.get('segregation_supervisor_uid')
            drop_driver_uid = request.data.get('drop_driver_uid')
            college_supervisor_uid = request.data.get('college_supervisor_uid')

            # Update related employees if provided
           
            if campus_uid:
                try:
                    campus_instance = Campus.objects.get(uid=campus_uid)
                    collection_instance.campus = campus_instance
                except Campus.DoesNotExist:
                    return Response({'error': 'Campus not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if supervisor_uid:
                try:
                    supervisor_instance = Employee.objects.get(uid=supervisor_uid)
                    collection_instance.supervisor = supervisor_instance
                except Employee.DoesNotExist:
                    return Response({'error': 'supervisor not found'}, status=status.HTTP_404_NOT_FOUND)


            if drying_supervisor_uid:
                try:
                    drying_supervisor_instance = Employee.objects.get(uid=drying_supervisor_uid)
                    collection_instance.drying_supervisor = drying_supervisor_instance
                except Employee.DoesNotExist:
                    return Response({'error': 'Drying supervisor not found'}, status=status.HTTP_404_NOT_FOUND)

            if segregation_supervisor_uid:
                try:
                    segregation_supervisor_instance = Employee.objects.get(uid=segregation_supervisor_uid)
                    collection_instance.segregation_supervisor = segregation_supervisor_instance
                except Employee.DoesNotExist:
                    return Response({'error': 'Segregation supervisor not found'}, status=status.HTTP_404_NOT_FOUND)

            if drop_driver_uid:
                try:
                    drop_driver_instance = Employee.objects.get(uid=drop_driver_uid)
                    collection_instance.drop_driver = drop_driver_instance
                except Employee.DoesNotExist:
                    return Response({'error': 'Drop driver not found'}, status=status.HTTP_404_NOT_FOUND)

            if college_supervisor_uid:
                try:
                    college_supervisor_instance = Employee.objects.get(uid=college_supervisor_uid)
                    collection_instance.college_supervisor = college_supervisor_instance
                except Employee.DoesNotExist:
                    return Response({'error': 'College supervisor not found'}, status=status.HTTP_404_NOT_FOUND)

            # Update related nested objects if provided
            if 'student_day_sheet' in request.data:
                collection_instance.student_day_sheet.clear()
                student_day_sheet = json.loads(request.data.get('student_day_sheet', '[]'))
                for student_day in student_day_sheet:
                    student_day_sheet_serializer = StudentDaySheetSerializer(data=student_day)
                    if student_day_sheet_serializer.is_valid():
                        student_day_sheet_instance = student_day_sheet_serializer.save()
                        collection_instance.student_day_sheet.add(student_day_sheet_instance)

            if 'faculty_day_sheet' in request.data:
                collection_instance.faculty_day_sheet.clear()
                faculty_day_sheet = json.loads(request.data.get('faculty_day_sheet', '[]'))
                for faculty_day in faculty_day_sheet:
                    faculty_day_sheet_serializer = FacultyDaySheetSerializer(data=faculty_day)
                    if faculty_day_sheet_serializer.is_valid():
                        faculty_day_sheet_instance = faculty_day_sheet_serializer.save()
                        collection_instance.faculty_day_sheet.add(faculty_day_sheet_instance)

            # Handle remarks update
            if 'student_remark' in request.data:
                collection_instance.student_remark.clear()
                student_remark_list = json.loads(request.data.get('student_remark', '[]'))
                for student_remark in student_remark_list:
                    student_remark_serializer = StudentRemarkSerializer(data=student_remark)
                    if student_remark_serializer.is_valid():
                        student_remark_instance = student_remark_serializer.save()
                        collection_instance.student_remark.add(student_remark_instance)

            if 'warehouse_remark' in request.data:
                collection_instance.warehouse.clear()
                warehouse_remark_list = json.loads(request.data.get('warehouse_remark', '[]'))
                for warehouse_remark in warehouse_remark_list:
                    warehouse_remark_serializer = RemarkByWarehouseSerializer(data=warehouse_remark)
                    if warehouse_remark_serializer.is_valid():
                        warehouse_remark_instance = warehouse_remark_serializer.save()
                        collection_instance.warehouse.add(warehouse_remark_instance)

            # Handle daily images update
            if 'daily_image_sheet' in request.FILES:
                collection_instance.daily_image_sheet.clear()
                daily_image_sheet_file = request.FILES.getlist('daily_image_sheet')
                for image_file in daily_image_sheet_file:
                    image_serializer = DailyImageSheetSerializer(data={'image': image_file})
                    if image_serializer.is_valid():
                        daily_image_instance = image_serializer.save()
                        collection_instance.daily_image_sheet.add(daily_image_instance)

            collection_instance.save()

            collection_serializer = CollectionSerializer(collection_instance)
            return Response({"message": "Collection updated successfully", "data": collection_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

   

    def delete(self, request, uid=None):
        try:
            collection_instance = Collection.objects.get(uid=uid)
            collection_instance.delete()
            return Response({"message": "Collection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Collection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)
   
    def retrieve(self, request, uid=None):
        try:
            collection_instance = Collection.objects.get(uid=uid)
            collection_serializer = CollectionSerializer(collection_instance)
            return Response({"message": "Collection retrieved successfully", "data": collection_serializer.data}, status=status.HTTP_200_OK)
        except Collection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

            

    def list(self, request):
        collections = Collection.objects.all()
        collection_serializer = CollectionSerializer(collections, many=True)
        return Response({"message": "Collections retrieved successfully", "data": collection_serializer.data}, status=status.HTTP_200_OK)


# step2

class GetCampusDetailsByUIDsViewset(viewsets.GenericViewSet):
    def get(self,request,uid):
        try:
            # Fetch colleges associated with the employee UID
            colleges = College.objects.filter(campus_employee__uid=uid).distinct()

            if not colleges.exists():
                return Response(
                    {"message": "No college found for the provided employee UID."},
                    status=status.HTTP_404_NOT_FOUND
                )

            college_campus_details = []

            for college in colleges:
                # Get all campuses associated with the filtered college
                campuses = Campus.objects.filter(college=college)

                # Serialize the college and associated campuses
                college_serializer = CollegeSerializer(college)
                campus_serializer = GetCampusSerializer(campuses, many=True)

                college_campus_details.append({
                    "college": college_serializer.data,
                    "campuses": campus_serializer.data
                })

            return Response(
                {
                    "message": "College and associated campuses fetched successfully through the employee uid.",
                    "data": college_campus_details
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching college and campus details.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetFacultyListViewset(viewsets.GenericViewSet):
    def get(self,request,uid):
        try:
            faculty_instance = Faculty.objects.filter(campus__uid = uid)
            faculty_serializer = FacultySerializer(faculty_instance,many=True)
            return Response({"message": "Faculty List", "data": faculty_serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': 'Faculty List Not Found'}, status=status.HTTP_404_NOT_FOUND)
        



class GetEmployeeCollectionsViewset(viewsets.GenericViewSet):
    def get(self, request, uid):
        try:
            # Filter collections by any of the employee-related fields using the employee UID
            collections = Collection.objects.filter(
                Q(supervisor__uid=uid) |
                Q(pickup_driver__uid=uid) |
                Q(washing_supervisor__uid=uid) |
                Q(drying_supervisor__uid=uid) |
                Q(segregation_supervisor__uid=uid) |
                Q(drop_driver__uid=uid) |
                Q(college_supervisor__uid=uid)
            )

            if not collections.exists():
                return Response(
                    {"message": "No collections found for the provided employee UID."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize the collections
            collection_serializer = CollectionSerializer(collections, many=True)

            return Response(
                {"message": "Employee Collections", "data": collection_serializer.data},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            # Handle any unexpected errors
            return Response(
                {"error": "An error occurred while retrieving the collections.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


class GetStudentDetailsViewset(viewsets.GenericViewSet):
    def post(self, request):
        tag_number = request.data.get('tag_number')
        campus_uid = request.data.get('campus_uid')

        if not tag_number or not campus_uid:
            return Response(
                {"error": "Both tag_number and campus_uid must be provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the campus instance using the provided UID
            campus_instance = get_object_or_404(Campus, uid=campus_uid)
            
            # Fetch the student using the tag_number and campus
            student_instance = get_object_or_404(Student, tag_number=tag_number, campus=campus_instance)
            
            # Serialize the student instance
            student_serializer = StudentSerializer(student_instance)
            
            return Response(
                {"message": "Student Details", "data": student_serializer.data},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            # Handle any unexpected errors
            return Response(
                {"error": "An error occurred while retrieving the student details.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


class LatestCollectionViewset(viewsets.GenericViewSet):
    def get(self, request):
        try:
            # Retrieve the latest collection based on the created_at field
            latest_collection = Collection.objects.latest('created_at')
            
            return Response(
                {"latest_collection_id": latest_collection.id},
                status=status.HTTP_200_OK
            )
        
        except Collection.DoesNotExist:
            return Response(
                {"message": "No collections found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        except Exception as e:
            return Response(
                {"error": "An error occurred while retrieving the latest collection.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class FilterCollectionsByStudentViewset(viewsets.GenericViewSet):
    def post(self, request):
        tag_number = request.data.get('tag_number')
        campus_uid = request.data.get('campus_uid')

        if not tag_number or not campus_uid:
            return Response(
                {"error": "Both tag_number and campus_uid must be provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Filter collections based on campus UID and tag_number in the related StudentDaySheet model
            collection_instance = Collection.objects.filter(
                campus__uid=campus_uid, 
                student_day_sheet__tag_number=tag_number 
            )

            undelivered_day_sheets_collection = collection_instance.filter(
                student_day_sheet__delivered=False
            )

            if undelivered_day_sheets_collection.exists():
                # Serialize collections
                collection_serializer = CollectionSerializer(undelivered_day_sheets_collection, many=True)
                
                return Response(
                    {
                        "message": "Filtered Collections where Student Day Sheets are undelivered",
                        "collections": collection_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "No undelivered student day sheets found for this student."},
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            return Response(
                {"error": "An error occurred while filtering collections.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DriverCollectionViewset(viewsets.GenericViewSet):
    def get(self, request, uid):
        try:
            employee_instance = Employee.objects.get(uid=uid)
            if employee_instance.employee_type != "Driver":
                return Response({"error": "Employee is not a driver."}, status=status.HTTP_400_BAD_REQUEST)
            # Get all Routes instances associated with the employee UID
            routes_instances = Routes.objects.filter(employee__uid=uid)

            if not routes_instances.exists():
                return Response({"error": "No routes found for the given employee UID."}, status=status.HTTP_404_NOT_FOUND)

            # Initialize an empty list to store all filtered collections
            filtered_collections = []

            # Iterate through each routes instance
            for routes_instance in routes_instances:
                # Get the list of colleges associated with each routes instance
                college_instances = College.objects.filter(routes=routes_instance)
                
                for college in college_instances:
                    campus_instances = Campus.objects.filter(college=college)
                    for campus in campus_instances:
                        collection_instances = Collection.objects.filter(campus=campus)

                        # Filter collections based on the statuses: READY_TO_PICK, IN_TRANSIT, READY_FOR_DELIVERY
                        filtered_collection = collection_instances.filter(
                            Q(current_status="READY_TO_PICK") |
                            Q(current_status="IN_TRANSIT") |
                            Q(current_status="READY_FOR_DELIVERY")
                        )

                        # Add the filtered collections to the list
                        filtered_collections.extend(filtered_collection)

            # Serialize the filtered collections
            serializer_collection = CollectionSerializer(filtered_collections, many=True)

            # Return the serialized data
            return Response({'data': serializer_collection.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "An error occurred while retrieving collections.", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class CollectionTaskviewset(viewsets.GenericViewSet):
    
    def get(self, request):
        serializer = CollectionTaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            request_status = serializer.validated_data.get("current_status")

            collection_instances = Collection.objects.none()

            # Filter collections based on the request status
            if request_status == "DELIVERED_TO_WAREHOUSE":
                collection_instances = Collection.objects.filter(current_status="WASHING")
            elif request_status == "WASHING_DONE":
                collection_instances = Collection.objects.filter(current_status="DRYING")
            elif request_status == "DRYING_DONE":
                collection_instances = Collection.objects.filter(current_status="IN_SEGREGATION")
            else:
                return Response({"error":"Invalid status"},status=status.HTTP_400_BAD_REQUEST)  
            

            collection_serializer = CollectionSerializer(collection_instances, many=True)
            return Response({"data": collection_serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
