from rest_framework import viewsets, status
from rest_framework.response import Response
from college.models import (Employee, College,Campus,Faculty,Student,
                            WashingMashine, DryingMashine,Vehicle, VehicleExpenses,FoldingTable,
                            complaint
                            )
from .serializers import (EmployeeSerializer, EmployeeDailyImageSerializer, 
                          CollegeSerializer, CampusSerializer,
                          FacultySerializer,StudentSerializer,
                          WashingMashineSerializer,WashingMashineCleanImageSerializer,
                          DryingMashineSerializer,VehicleSerializer,VehicleExpensesSerializer,
                          FoldingTableSerializer,complaintSerializer
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