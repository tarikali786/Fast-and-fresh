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
                            RemarkByWarehouse,Routes,DryArea,FilldArea,PreviousStatus, OtherclothDaySheet
                            )
from .serializers import (EmployeeSerializer, EmployeeDailyImageSerializer, 
                          CollegeSerializer, CampusSerializer,
                          FacultySerializer,StudentSerializer,
                          WashingMashineSerializer,WashingMashineCleanImageSerializer,
                          DryingMashineSerializer,VehicleSerializer,VehicleExpensesSerializer,
                          FoldingTableSerializer,complaintSerializer,CollectionSerializer,
                          DailyImageSheetSerializer,StudentDaySheetSerializer,FacultyDaySheetSerializer,
                          StudentRemarkSerializer,RemarkByWarehouseSerializer,
                          EmployeeSignInserializer,GetCampusSerializer,RoutesSerializer,
                          LogisticbagNumberSerializer,FacultybagNumbersSerializer,DryAreaSerializer,
                          CollectionResponseSerializer,FilldAreaSerializer,OtherclothDaySheetSerializer,
                          OtherClothBagNumberSerializer
                          )


class EmployeeViewSet(viewsets.GenericViewSet):
    def create(self, request):
        email = request.data.get("email")
        if Employee.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            serializer = EmployeeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                employee = serializer.save()

                # Handle the uploaded daily images from request.FILES
                daily_images_files = request.FILES.getlist('daily_images')
                for image_file in daily_images_files:
                    image_serializer = EmployeeDailyImageSerializer(data={'image': image_file})
                    if image_serializer.is_valid(raise_exception=True):
                        daily_image_instance = image_serializer.save()
                        employee.daily_images.add(daily_image_instance)

                return Response({"message": "Employee created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            

    def delete(self,request,uid):
        employee = get_object_or_404(Employee, uid=uid)
        employee.delete()
        return Response({"message":f'{employee.name} is successfully delete'},status=status.HTTP_200_OK)


class AllEmployeeViewset(viewsets.GenericViewSet):
    
    def get(self, request):
        query = request.GET.get('q')  
        if query:
            employees = Employee.objects.filter(employee_type=query)
        else:
            employees = Employee.objects.all()
            
        serializer = EmployeeSerializer(employees, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    
class EmployeeLogoutViewset(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def logout(self, request):
        try:
            # Blacklist the refresh token
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Log the user out and clear session
            logout(request)

            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

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

                return Response({"data":employee_data.data,"refresh_token": str(refresh), "access_token": str(refresh.access_token)}, status=200)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
            
                                
        else:
            return Response({"error": "Employee not found"}, status=status.HTTP_400_BAD_REQUEST)
        

class EmployeeUpdateViewset(viewsets.GenericViewSet):
    def update(self,request,uid):
        employee = Employee.objects.get(uid=uid)
        serializer = EmployeeSerializer(employee, data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Employee updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




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
        if serializer.is_valid(raise_exception=True):
            washing_mashine = serializer.save()

            before_and_after_cleaned_image_files = request.FILES.getlist('before_and_after_cleaned_image')
            for image_file in before_and_after_cleaned_image_files:
                image_serializer = WashingMashineCleanImageSerializer(data={'image': image_file})
                if image_serializer.is_valid(raise_exception=True):
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
            
            if serializer.is_valid(raise_exception=True):
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
        if serializer.is_valid(raise_exception=True):
            washing_mashine = serializer.save()

            # Handle the before_and_after_cleaned_image files
            before_and_after_cleaned_image_files = request.FILES.getlist('before_and_after_cleaned_image')
            for image_file in before_and_after_cleaned_image_files:
                image_serializer = WashingMashineCleanImageSerializer(data={'image': image_file})
                if image_serializer.is_valid(raise_exception=True):
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

            if serializer.is_valid(raise_exception=True):
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


class VehicleUpdateViewset(viewsets.GenericViewSet):

    def update(self, request):
        last_driver_id = request.data.get("last_driver_uid")
        vehicle_id = request.data.get("vehicle_uid")
        odo_meter_image = request.data.get("odo_meter_image")

        if not last_driver_id or not vehicle_id:
            return Response({"error": "last_driver_uid or vehicle_uid not found!"}, status=status.HTTP_400_BAD_REQUEST)

        last_driver = get_object_or_404(Employee, uid=last_driver_id)

        vehicle= get_object_or_404(Vehicle, uid=vehicle_id)
        serialize = VehicleSerializer(vehicle,data=request.data,partial=True)
        if serialize.is_valid(raise_exception=True):
            vehicle_instance = serialize.save()

            vehicle_instance.last_driver = last_driver
            if odo_meter_image:
                vehicle_instance.odo_meter_image = odo_meter_image

            vehicle_instance.save()

            serializer = VehicleSerializer(vehicle_instance)

            return Response({"message": "Vehicle updated", "data": serializer.data}, status=status.HTTP_200_OK)

        
         




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

            

            # Update the ETA based on the college's schedule
            collection_instance.ETA = college_instance.schedule
            if collection_instance.isActive ==False:
                collection_instance.isActive = True
                

            collection_instance.save()
            
            # Save nested related objects
            student_day_sheet= json.loads(request.data.get('student_day_sheet', '[]'))
            for student_day in student_day_sheet:
                student_day_sheet_serializer = StudentDaySheetSerializer(data=student_day)
                if student_day_sheet_serializer.is_valid(raise_exception=True):
                    student_day_sheet_instance = student_day_sheet_serializer.save()
                    collection_instance.student_day_sheet.add(student_day_sheet_instance)


            faculty_day_sheet = json.loads(request.data.get('faculty_day_sheet', '[]'))
            for faculty_day in faculty_day_sheet:
                faculty_day_sheet_serializer = FacultyDaySheetSerializer(data=faculty_day)
                if faculty_day_sheet_serializer.is_valid(raise_exception=True):
                    faculty_day_sheet_instance = faculty_day_sheet_serializer.save()
                    collection_instance.faculty_day_sheet.add(faculty_day_sheet_instance)
                else:
                    return Response(faculty_day_sheet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



            student_remark_list  = json.loads(request.data.get('student_remark', '[]'))
            if student_remark_list is not None:
                for student_remark in student_remark_list:
                    student_remark_serializer = FacultyDaySheetSerializer(data=student_remark)
                    if student_remark_serializer.is_valid(raise_exception=True):
                        student_remark_instance = student_remark_serializer.save()
                        collection_instance.student_remark.add(student_remark_instance)

            warehouse_remark_list  = json.loads(request.data.get('student_remark', '[]'))
            if student_remark_list is not None:
                for warehouse_remark in warehouse_remark_list:
                    warehouse_remark_serializer = FacultyDaySheetSerializer(data=warehouse_remark)
                    if warehouse_remark_serializer.is_valid(raise_exception=True):
                        warehouse_remark_instance = warehouse_remark_serializer.save()
                        collection_instance.warehouse.add(warehouse_remark_instance)

            if "other_cloth_daysheet" in request.data:
                other_cloth_daysheet_list =  json.loads(request.data.get('other_cloth_daysheet', []))
                for other_c_daysheet in other_cloth_daysheet_list:
                    other_c_serializer = OtherclothDaySheetSerializer(data=other_c_daysheet)
                    if other_c_serializer.is_valid(raise_exception=True):
                        other_cloth_daysheet_instance=other_c_serializer.save()
                        collection_instance.other_cloth_daysheet.add(other_cloth_daysheet_instance)


            
            # Handle the uploaded daily images from request.FILES
            daily_image_sheet_file = request.FILES.getlist('daily_image_sheet')
            for image_file in daily_image_sheet_file:
                image_serializer = DailyImageSheetSerializer(data={'image': image_file})
                if image_serializer.is_valid(raise_exception=True):
                    daily_image_instance = image_serializer.save()
                    collection_instance.daily_image_sheet.add(daily_image_instance)

            
            collection_instance.save()
            
            collection_serializer = CollectionResponseSerializer(collection_instance)
            return Response({"message": "Collection created successfully", "data": collection_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)



    def update(self, request, uid=None):

        current_status = request.data.get("current_status")

        try:
            collection_instance = Collection.objects.get(uid=uid)

            if current_status and collection_instance:

                if collection_instance.current_status ==current_status:
                    pass
                else:
               
                    previous_status_instance = PreviousStatus.objects.create(
                        status=collection_instance.current_status,
                        updated_time=collection_instance.updated_at
                    )
    
                    collection_instance.previous_status.add(previous_status_instance)


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
            pickup_driver_uid = request.data.get('pickup_driver_uid')
            washing_supervisor_uid = request.data.get('washing_supervisor_uid')

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
                    if supervisor_instance.employee_type =="Campus_Employee":
                        collection_instance.supervisor = supervisor_instance
                    else:
                        return Response({"error":"Employe type is not Campus supervisor or campus emplopyee"})
                except Employee.DoesNotExist:
                    return Response({'error': 'supervisor not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if washing_supervisor_uid:
                try:
                    supervisor_instance = Employee.objects.get(uid=washing_supervisor_uid)
                    if supervisor_instance.employee_type =="Washing":
                        collection_instance.washing_supervisor = supervisor_instance
                    else:
                        return Response({"error":"Employe type is not Washing supervisor"})
                except Employee.DoesNotExist:
                    return Response({'error': 'supervisor not found'}, status=status.HTTP_404_NOT_FOUND)


            if drying_supervisor_uid:
                try:
                    drying_supervisor_instance = Employee.objects.get(uid=drying_supervisor_uid)
                    if drying_supervisor_instance.employee_type =="Drying":
                        collection_instance.drying_supervisor = drying_supervisor_instance
                    else:
                        return Response({"error":"Employe type is not Drying supervisor"})
                except Employee.DoesNotExist:
                    return Response({'error': 'Drying supervisor not found'}, status=status.HTTP_404_NOT_FOUND)

            if segregation_supervisor_uid:
                try:
                    
                    segregation_supervisor_instance = Employee.objects.get(uid=segregation_supervisor_uid)
                    if segregation_supervisor_instance.employee_type =="Segregation":
                        collection_instance.segregation_supervisor = segregation_supervisor_instance
                    else:
                        return Response({"error":"Employe type is not Segregation supervisor"})
                except Employee.DoesNotExist:
                    return Response({'error': 'Segregation supervisor not found'}, status=status.HTTP_404_NOT_FOUND)

            if drop_driver_uid:
                try:
                    drop_driver_instance = Employee.objects.get(uid=drop_driver_uid)
                    if drop_driver_instance.employee_type =="Driver":
                    
                        collection_instance.drop_driver = drop_driver_instance
                    else:
                        return Response({"error":"Employe type is not  driver"})
                except Employee.DoesNotExist:
                    return Response({'error': 'Drop driver not found'}, status=status.HTTP_404_NOT_FOUND)

            if pickup_driver_uid:
                try:
                    pickup_driver_instance = Employee.objects.get(uid=pickup_driver_uid)
                    if pickup_driver_instance.employee_type =="Driver":
                        collection_instance.pickup_driver = pickup_driver_instance
                    else:
                        return Response({"error":"Employe type is not  driver"})
                except Employee.DoesNotExist:
                    return Response({'error': 'Drop driver not found'}, status=status.HTTP_404_NOT_FOUND)


            


            if 'student_day_sheet' in request.data:
                student_day_sheet = json.loads(request.data.get('student_day_sheet', '[]'))

                for student_day in student_day_sheet:
                    s_uid = student_day.get('uid')

                    if s_uid:
                        try:
                            student_day_sheet_instance = StudentDaySheet.objects.get(uid=s_uid)

                            student_day_sheet_serializer = StudentDaySheetSerializer(student_day_sheet_instance, data=student_day, partial=True)
                            if student_day_sheet_serializer.is_valid(raise_exception=True):
                                student_day_sheet_serializer.save()

                        except StudentDaySheet.DoesNotExist:
                            student_day_sheet_serializer = StudentDaySheetSerializer(data=student_day)
                            if student_day_sheet_serializer.is_valid(raise_exception=True):
                                student_day_sheet_instance = student_day_sheet_serializer.save()
                                collection_instance.student_day_sheet.add(student_day_sheet_instance)
                    else:
                        student_day_sheet_serializer = StudentDaySheetSerializer(data=student_day)
                        if student_day_sheet_serializer.is_valid(raise_exception=True):
                            student_day_sheet_instance = student_day_sheet_serializer.save()
                            collection_instance.student_day_sheet.add(student_day_sheet_instance)





            if 'faculty_day_sheet' in request.data:
                faculty_day_sheet = json.loads(request.data.get('faculty_day_sheet', '[]'))

                for faculty_day in faculty_day_sheet:
                    f_day_sheet_uid = faculty_day.get('uid')

                    if f_day_sheet_uid:
                        try:
                            faculty_instance = FacultyDaySheet.objects.get(uid=f_day_sheet_uid)
                            faculty_day_sheet_serializer = FacultyDaySheetSerializer(faculty_instance, data=faculty_day, partial=True)
                            if faculty_day_sheet_serializer.is_valid(raise_exception=True):
                                faculty_day_sheet_serializer.save()
                        except FacultyDaySheet.DoesNotExist:
                            faculty_day_sheet_serializer = FacultyDaySheetSerializer(data=faculty_day)
                            if faculty_day_sheet_serializer.is_valid(raise_exception=True):
                                faculty_day_sheet_instance = faculty_day_sheet_serializer.save()
                                collection_instance.faculty_day_sheet.add(faculty_day_sheet_instance)
                    else:
                        faculty_day_sheet_serializer = FacultyDaySheetSerializer(data=faculty_day)
                        if faculty_day_sheet_serializer.is_valid(raise_exception=True):
                            faculty_day_sheet_instance = faculty_day_sheet_serializer.save()
                            collection_instance.faculty_day_sheet.add(faculty_day_sheet_instance)

                        




            # Handle remarks update
            if 'student_remark' in request.data:
                student_remark_list = json.loads(request.data.get('student_remark', '[]'))
                for student_remark in student_remark_list:
                    student_remark_serializer = StudentRemarkSerializer(data=student_remark)
                    if student_remark_serializer.is_valid(raise_exception=True):
                        student_remark_instance = student_remark_serializer.save()
                        collection_instance.student_remark.add(student_remark_instance)

            if 'warehouse_remark' in request.data:
                warehouse_remark_list = json.loads(request.data.get('warehouse_remark', '[]'))
                for warehouse_remark in warehouse_remark_list:
                    warehouse_remark_serializer = RemarkByWarehouseSerializer(data=warehouse_remark)
                    if warehouse_remark_serializer.is_valid(raise_exception=True):
                        warehouse_remark_instance = warehouse_remark_serializer.save()
                        collection_instance.warehouse_remark.add(warehouse_remark_instance)

            # Handle daily images update
            if 'daily_image_sheet' in request.FILES:
                daily_image_sheet_file = request.FILES.getlist('daily_image_sheet')
                for image_file in daily_image_sheet_file:
                    image_serializer = DailyImageSheetSerializer(data={'image': image_file})
                    if image_serializer.is_valid(raise_exception=True):
                        daily_image_instance = image_serializer.save()
                        collection_instance.daily_image_sheet.add(daily_image_instance)

            
            # Handle campus_pickup_bag_numbers update
            if 'campus_pickup_bag_numbers' in request.data:
                campus_pickup_bag_numbers_list =  json.loads(request.data.get('campus_pickup_bag_numbers', []))
                for campus_pickup_bag in campus_pickup_bag_numbers_list:
                    campus_pickup_bag_number_serializer = LogisticbagNumberSerializer(data=campus_pickup_bag)
                    if campus_pickup_bag_number_serializer.is_valid(raise_exception=True):
                        campus_pickup_bag_number_instance = campus_pickup_bag_number_serializer.save()
                        collection_instance.campus_pickup_bag_numbers.add(campus_pickup_bag_number_instance)

            if 'warehouse_pickup_bag_numbers' in request.data:
                warehouse_pickup_bag_numbers_list =  json.loads(request.data.get('warehouse_pickup_bag_numbers', []))
                for warehouse_pickup_bag in warehouse_pickup_bag_numbers_list:
                    warehouse_pickup_bag_number_serializer = LogisticbagNumberSerializer(data=warehouse_pickup_bag)
                    if warehouse_pickup_bag_number_serializer.is_valid(raise_exception=True):
                        warehouse_pickup_bag_number_instance =warehouse_pickup_bag_number_serializer.save()
                        collection_instance.warehouse_pickup_bag_numbers.add(warehouse_pickup_bag_number_instance)


            if 'campus_drop_bag_numbers' in request.data:
                campus_drop_bag_numbers_list =  json.loads(request.data.get('campus_drop_bag_numbers', []))
                for campus_drop_bag in campus_drop_bag_numbers_list:
                    campus_drop_bag_number_serializer = LogisticbagNumberSerializer(data=campus_drop_bag)
                    if campus_drop_bag_number_serializer.is_valid(raise_exception=True):
                        campus_drop_bag_number_instance = campus_drop_bag_number_serializer.save()
                        collection_instance.campus_drop_bag_numbers.add(campus_drop_bag_number_instance)

            if 'warehouse_drop_bag_numbers' in request.data:
                warehouse_drop_bag_numbers_list =  json.loads(request.data.get('warehouse_drop_bag_numbers', []))
                for warehouse_drop_bag in warehouse_drop_bag_numbers_list:
                    warehouse_drop_bag_number_serializer = LogisticbagNumberSerializer(data=warehouse_drop_bag)
                    if warehouse_drop_bag_number_serializer.is_valid(raise_exception=True):
                        warehouse_drop_bag_number_instance = warehouse_drop_bag_number_serializer.save()
                        collection_instance.warehouse_drop_bag_numbers.add(warehouse_drop_bag_number_instance)

            
        
            
            # Handle campus_pickup_faculty_bag_number update
            if 'campus_pickup_faculty_bag_number' in request.data:
                campus_pickup_faculty_bag_numbers_list =  json.loads(request.data.get('campus_pickup_faculty_bag_number', []))
                for campus_pickup_faculty_bag in campus_pickup_faculty_bag_numbers_list:
                    campus_pickup_faculty_bag_number_serializer = FacultybagNumbersSerializer(data=campus_pickup_faculty_bag)
                    if campus_pickup_faculty_bag_number_serializer.is_valid(raise_exception=True):
                        campus_pickup_faculty_bag_number_instance = campus_pickup_faculty_bag_number_serializer.save()
                        collection_instance.campus_pickup_faculty_bag_number.add(campus_pickup_faculty_bag_number_instance)

            if 'campus_drop_faculty_bag_number' in request.data:
                warehouse_pickup_faculty_bag_numbers_list =  json.loads(request.data.get('campus_drop_faculty_bag_number', []))
                for warehouse_pickup_faculty_bag in warehouse_pickup_faculty_bag_numbers_list:
                    warehouse_pickup_faculty_bag_number_serializer = FacultybagNumbersSerializer(data=warehouse_pickup_faculty_bag)
                    if warehouse_pickup_faculty_bag_number_serializer.is_valid(raise_exception=True):
                        warehouse_pickup_faculty_bag_number_instance =warehouse_pickup_faculty_bag_number_serializer.save()
                        collection_instance.campus_drop_faculty_bag_number.add(warehouse_pickup_faculty_bag_number_instance)


            if 'warehouse_pickup_faculty_bag_number' in request.data:
                campus_drop_faculty_bag_numbers_list =  json.loads(request.data.get('warehouse_pickup_faculty_bag_number', []))
                for campus_drop_faculty_bag in campus_drop_faculty_bag_numbers_list:
                    campus_drop_faculty_bag_number_serializer = FacultybagNumbersSerializer(data=campus_drop_faculty_bag)
                    if campus_drop_faculty_bag_number_serializer.is_valid(raise_exception=True):
                        campus_drop_faculty_bag_number_instance = campus_drop_faculty_bag_number_serializer.save()
                        collection_instance.warehouse_pickup_faculty_bag_number.add(campus_drop_faculty_bag_number_instance)

            if 'warehouse_drop_faculty_bag_number' in request.data:
                warehouse_drop_faculty_bag_numbers_list =  json.loads(request.data.get('warehouse_drop_faculty_bag_number', []))
                for warehouse_drop_faculty_bag in warehouse_drop_faculty_bag_numbers_list:
                    warehouse_drop_faculty_bag_number_serializer = FacultybagNumbersSerializer(data=warehouse_drop_faculty_bag)
                    if warehouse_drop_faculty_bag_number_serializer.is_valid(raise_exception=True):
                        warehouse_drop_faculty_bag_number_instance = warehouse_drop_faculty_bag_number_serializer.save()
                        collection_instance.warehouse_drop_faculty_bag_number.add(warehouse_drop_faculty_bag_number_instance)


            if "other_cloth_daysheet" in request.data:
                other_cloth_daysheet_list =  json.loads(request.data.get('other_cloth_daysheet', []))
                for other_c_daysheet in other_cloth_daysheet_list:
                    other_uid = other_c_daysheet.get("uid")
                    if other_uid:
                        try:
                            other_cloth_daysheet_instance = OtherclothDaySheet.objects.get(uid=other_uid)
                            other_c_serializer = OtherclothDaySheetSerializer(other_cloth_daysheet_instance, data=other_c_daysheet, partial=True)
                            if other_c_serializer.is_valid(raise_exception=True):
                                other_c_serializer.save()
                        except OtherclothDaySheet.DoesNotExist:
                            return Response ({"error":"Other Cloth Daysheet uid does not exist"})
                        
                    else:
                        other_cloth_daysheet_serializer = OtherclothDaySheetSerializer(data=other_c_daysheet)
                        if other_cloth_daysheet_serializer.is_valid(raise_exception=True):
                            other_cloth_daysheet_instance = other_cloth_daysheet_serializer.save()
                            collection_instance.other_cloth_daysheet.add(other_cloth_daysheet_instance)


            if 'other_cloth_campus_pickup' in request.data:
                other_cloth_campus_pickup_list =  json.loads(request.data.get('other_cloth_campus_pickup', []))
                for other_cloth_campus_pick in other_cloth_campus_pickup_list:
                    other_cloth_campus_pickup_serializer = OtherClothBagNumberSerializer(data=other_cloth_campus_pick)
                    if other_cloth_campus_pickup_serializer.is_valid(raise_exception=True):
                        other_cloth_campus_pickup_instance = other_cloth_campus_pickup_serializer.save()
                        collection_instance.other_cloth_campus_pickup.add(other_cloth_campus_pickup_instance)

            if 'other_cloth_campus_drop' in request.data:
                other_cloth_campus_drop_list =  json.loads(request.data.get('other_cloth_campus_drop', []))
                for other_cloth_campus_drop in other_cloth_campus_drop_list:
                    other_cloth_campus_drop_serializer = OtherClothBagNumberSerializer(data=other_cloth_campus_drop)
                    if other_cloth_campus_drop_serializer.is_valid(raise_exception=True):
                        other_cloth_campus_drop_instance = other_cloth_campus_drop_serializer.save()
                        collection_instance.other_cloth_campus_drop.add(other_cloth_campus_drop_instance)

            if 'other_cloth_warehouse_pickup' in request.data:
                other_cloth_warehouse_pickup_list =  json.loads(request.data.get('other_cloth_warehouse_pickup', []))
                for other_cloth_warehouse_pick in other_cloth_warehouse_pickup_list:
                    other_cloth_warehouse_pickup_serializer = OtherClothBagNumberSerializer(data=other_cloth_warehouse_pick)
                    if other_cloth_warehouse_pickup_serializer.is_valid(raise_exception=True):
                        other_cloth_warehouse_pickup_instance = other_cloth_warehouse_pickup_serializer.save()
                        collection_instance.other_cloth_warehouse_pickup.add(other_cloth_warehouse_pickup_instance)


            if 'other_cloth_warehouse_drop' in request.data:
                other_cloth_warehouse_drop_list =  json.loads(request.data.get('other_cloth_warehouse_drop', []))
                for other_cloth_warehouse_d in other_cloth_warehouse_drop_list:
                    other_cloth_warehouse_d_serializer = OtherClothBagNumberSerializer(data=other_cloth_warehouse_d)
                    if other_cloth_warehouse_d_serializer.is_valid(raise_exception=True):
                        other_cloth_warehouse_d_serializer_instance = other_cloth_warehouse_d_serializer.save()
                        collection_instance.other_cloth_warehouse_drop.add(other_cloth_warehouse_d_serializer_instance)


            collection_instance.save()

            collection_serializer = CollectionResponseSerializer(collection_instance)
           
            return Response({"message": "Collection updated successfully", "data": collection_serializer.data,}, status=status.HTTP_200_OK)
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
            collection_serializer = CollectionResponseSerializer(collection_instance)
            return Response({"message": "Collection retrieved successfully", "data": collection_serializer.data}, status=status.HTTP_200_OK)
        except Collection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

            

    def list(self, request):
        collections = Collection.objects.all()
        collection_serializer = CollectionResponseSerializer(collections, many=True)
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
                Q(drop_driver__uid=uid) 
            )

            if not collections.exists():
                return Response(
                    {"message": "No collections found for the provided employee UID."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize the collections
            collection_serializer = CollectionResponseSerializer(collections, many=True)

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
                student_day_sheet__tag_number=tag_number ,
                current_status__in=["DELIVERED_TO_CAMPUS", "DELIVERED_TO_STUDENT"]

            )

            undelivered_day_sheets_collection = collection_instance.filter(
                student_day_sheet__delivered=False
            )

            if undelivered_day_sheets_collection.exists():
                # Serialize collections
                collection_serializer = CollectionResponseSerializer(undelivered_day_sheets_collection, many=True)
                
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

            # Filter collections by the specified statuses
            filtered_collection_list = Collection.objects.filter(
                Q(current_status="READY_TO_PICK") |
                Q(current_status="INTRANSIT_FROM_cAMPUS") |
                Q(current_status="INTRANSIT_FROM_WAREHOUSE") |
                Q(current_status="READY_FOR_DELIVERY")
            )

            # Filter collections further by the route's employee
            filtered_collections = filtered_collection_list.filter(
                campus__college__routes__employee=employee_instance
            )

            # Serialize the filtered collections
            serializer = CollectionResponseSerializer(filtered_collections, many=True)

            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An error occurred while retrieving collections.", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CollectionTaskviewset(viewsets.GenericViewSet):
    
    def get(self, request,uid):
        employee_instance = Employee.objects.get(uid=uid)
        if employee_instance.employee_type == "Washing":
            collection_instances = Collection.objects.filter(Q(current_status="DELIVERED_TO_WAREHOUSE") | Q(current_status="WASHING") )
        
        elif employee_instance.employee_type == "Drying":
            collection_instances = Collection.objects.filter(Q(current_status="WASHING_DONE") | Q(current_status="DRYING"))
        
        elif employee_instance.employee_type == "Segregation":
            collection_instances = Collection.objects.filter(Q(current_status="DRYING_DONE") |Q(current_status="IN_SEGREGATION"))
            
        else:
            return Response ({"error":"Employee UID is not Valid"})
        
        collection_serializer = CollectionResponseSerializer(collection_instances, many=True)
        return Response({"data": collection_serializer.data}, status=status.HTTP_200_OK)
        


class DeliveredHistoryViewSet(viewsets.GenericViewSet):
    
    def get(self, request, uid):
        try:
            employee_instance = Employee.objects.get(uid=uid)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        if employee_instance.employee_type == "Driver":
            collection_instances = Collection.objects.filter(drop_driver=employee_instance, current_status="DELIVERED_TO_CAMPUS")
        
        elif employee_instance.employee_type == "Washing":
            collection_instances = Collection.objects.filter(drop_driver=employee_instance, current_status="DELIVERED_TO_CAMPUS")

        elif employee_instance.employee_type == "Drying":
            collection_instances = Collection.objects.filter(drop_driver=employee_instance, current_status="DELIVERED_TO_CAMPUS")
                 

        elif employee_instance.employee_type == "Segregation":
            collection_instances = Collection.objects.filter(drop_driver=employee_instance, current_status="DELIVERED_TO_CAMPUS")
                    
        serializer = CollectionResponseSerializer(collection_instances, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    


class DryAreaViewSet(viewsets.ModelViewSet):
    queryset = DryArea.objects.all()
    serializer_class = DryAreaSerializer
    lookup_field="uid"




class DryAreaUpdateViewSet(viewsets.GenericViewSet):
    def update(self, request, uid):
        try:
            dry_area_instance = DryArea.objects.get(uid=uid)
        except DryArea.DoesNotExist:
            return Response({"error": "Dry Area not found"}, status=status.HTTP_404_NOT_FOUND)
        
        dry_area_id= request.data.get('dry_area_id')
        row= request.data.get('row')
        column= request.data.get('column')
        
        if dry_area_id:
            dry_area_instance.dry_area_id = dry_area_id
            dry_area_instance.save()
        elif row:
            dry_area_instance.row = row
            dry_area_instance.save()
        elif column:
            dry_area_instance.column = column
            dry_area_instance.save()

        

        

        serializer = FilldAreaSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            fill_area_instance = serializer.save()
            dry_area_instance.fill_area = fill_area_instance
            dry_area_instance.save()
            serializer_value = DryAreaSerializer(dry_area_instance)
            return Response({"message": "Dry Area updated successfully","d":serializer_value.data}, status=status.HTTP_200_OK)
                            
        else:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)



class EmployeeActiveTaskViewset(viewsets.GenericViewSet):

    def get(self, request, uid):
        try:
            Emp_instance = Employee.objects.get(uid=uid)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        collection_list = Collection.objects.none()  

        if Emp_instance:
            if Emp_instance.employee_type == "Campus_Employee":
                collection_list = Collection.objects.filter(
                    supervisor=Emp_instance
                ).exclude(
                    current_status="DELIVERED_TO_STUDENT"
                )

            elif Emp_instance.employee_type == "Driver":
                pickup_collection_list = Collection.objects.filter(
                    pickup_driver=Emp_instance
                ).exclude(
                    current_status="DELIVERED_TO_STUDENT"
                )

                drop_collection_list = Collection.objects.filter(
                    drop_driver=Emp_instance
                ).exclude(
                    current_status="DELIVERED_TO_STUDENT"
                )

                collection_list = pickup_collection_list.union(drop_collection_list)

            elif Emp_instance.employee_type == "Washing":
                collection_list = Collection.objects.filter(
                    washing_supervisor=Emp_instance
                ).exclude(
                    current_status="DELIVERED_TO_STUDENT"
                )

            elif Emp_instance.employee_type == "Drying":
                collection_list = Collection.objects.filter(
                    drying_supervisor=Emp_instance
                ).exclude(
                    current_status="DELIVERED_TO_STUDENT"
                )

            elif Emp_instance.employee_type == "Segregation":
                collection_list = Collection.objects.filter(
                    segregation_supervisor=Emp_instance
                ).exclude(
                    current_status="DELIVERED_TO_STUDENT"
                )
            else:
                return Response({"error": "Invalid employee type"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = CollectionResponseSerializer(collection_list, many=True)
            return Response({"active_tasks": serializer.data}, status=status.HTTP_200_OK)
        
        else:
            return Response({"error": "Invalid Employee ID"}, status=status.HTTP_404_NOT_FOUND)




class EmployeeInActiveTaskViewset(viewsets.GenericViewSet):

    def get(self, request, uid):
        pagination_count = request.data.get("count", 10)  

        try:
            Emp_instance = Employee.objects.get(uid=uid)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        collection_list = Collection.objects.none()  

        if Emp_instance:
            if Emp_instance.employee_type == "Campus_Employee":
                collection_list = Collection.objects.filter(
                    supervisor=Emp_instance,
                    current_status="DELIVERED_TO_STUDENT"
                )

            elif Emp_instance.employee_type == "Driver":
                pickup_collection_list = Collection.objects.filter(
                    pickup_driver=Emp_instance,
                    current_status="DELIVERED_TO_STUDENT"
                )

                drop_collection_list = Collection.objects.filter(
                    drop_driver=Emp_instance,
                    current_status="DELIVERED_TO_STUDENT"
                )

                collection_list = pickup_collection_list.union(drop_collection_list)

            elif Emp_instance.employee_type == "Washing":
                collection_list = Collection.objects.filter(
                    washing_supervisor=Emp_instance,
                    current_status="DELIVERED_TO_STUDENT"
                )

            elif Emp_instance.employee_type == "Drying":
                collection_list = Collection.objects.filter(
                    drying_supervisor=Emp_instance,
                    current_status="DELIVERED_TO_STUDENT"
                )

            elif Emp_instance.employee_type == "Segregation":
                collection_list = Collection.objects.filter(
                    segregation_supervisor=Emp_instance,
                    current_status="DELIVERED_TO_STUDENT"
                )
            else:
                return Response({"error": "Invalid employee type"}, status=status.HTTP_400_BAD_REQUEST)

            # Apply pagination
            paginated_collection_list = collection_list[:pagination_count]

            serializer = CollectionResponseSerializer(paginated_collection_list, many=True)
            return Response({"inactive_tasks": serializer.data}, status=status.HTTP_200_OK)
        
        else:
            return Response({"error": "Invalid Employee ID"}, status=status.HTTP_404_NOT_FOUND)
