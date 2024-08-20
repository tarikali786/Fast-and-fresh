from rest_framework import serializers
from college.models import (Employee, EmployeeDailyImage,College,Campus,Faculty,Student,
                            WashingMashine, WashingMashineCleanImage,DryingMashine,DryingMashineCleanImage,
                            VehicleExpenses,Vehicle,FoldingTable,complaint,
                            DailyImageSheet,StudentDaySheet,FacultyDaySheet,
                            StudentRemark,RemarkByWarehouse,Collection
                            )
import uuid
class EmployeeDailyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDailyImage
        fields = ['image']

class EmployeeSerializer(serializers.ModelSerializer):
    daily_images = EmployeeDailyImageSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}





class CollegeSerializer(serializers.ModelSerializer):
    campus_employee = serializers.SlugRelatedField(
        queryset=Employee.objects.all(),
        many=True,
        slug_field='uid'
    )

    class Meta:
        model = College
        fields = ['uid', 'name', 'monthly_payment', 'delivery_time', 'schedule', 'campus_employee']

    def create(self, validated_data):
        # Pop the campus_employee data from validated_data
        employees_data = validated_data.pop('campus_employee', [])
        college = College.objects.create(**validated_data)
        # Set the campus_employee relationships
        college.campus_employee.set(employees_data) 
        return college
    



class CampusSerializer(serializers.ModelSerializer):
    college_uid = serializers.CharField(write_only=True, required=True)
    college = CollegeSerializer(read_only=True) 

    class Meta:
        model = Campus
        fields = '__all__'

    def create(self, validated_data):
        college_uid = validated_data.pop('college_uid', None)
        if college_uid:
            try:
                college = College.objects.get(uid=college_uid)
                validated_data['college'] = college
            except College.DoesNotExist:
                raise serializers.ValidationError({'college_uid': 'College with this UID does not exist.'})
        
        campus = super().create(validated_data)
        return campus

    def update(self, instance, validated_data):
        college_uid = validated_data.pop('college_uid', None)
        if college_uid:
            try:
                college = College.objects.get(uid=college_uid)
                instance.college = college
            except College.DoesNotExist:
                raise serializers.ValidationError({'college_uid': 'College with this UID does not exist.'})
        
        return super().update(instance, validated_data)


class FacultySerializer(serializers.ModelSerializer):
    college_uid = serializers.CharField(write_only=True, required=False)
    college = serializers.SlugRelatedField(
        queryset=College.objects.all(),
        slug_field='uid'
    )

    class Meta:
        model = Faculty
        fields = '__all__'

    def create(self, validated_data):
        college_uid = validated_data.pop('college_uid', None)
        if college_uid:
            try:
                college = College.objects.get(uid=college_uid)
                validated_data['college'] = college
            except College.DoesNotExist:
                raise serializers.ValidationError({'college_uid': 'College with this UID does not exist.'})
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        college_uid = validated_data.pop('college_uid', None)
        if college_uid:
            try:
                college = College.objects.get(uid=college_uid)
                instance.college = college
            except College.DoesNotExist:
                raise serializers.ValidationError({'college_uid': 'College with this UID does not exist.'})
        
        return super().update(instance, validated_data)



class StudentSerializer(serializers.ModelSerializer):
    campus_uid = serializers.CharField(write_only=True, required=False)
    campus = serializers.SlugRelatedField(
        queryset=Campus.objects.all(),
        slug_field='uid'
    )

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        campus_uid = validated_data.pop('campus_uid', None)
        if campus_uid:
            try:
                campus = Campus.objects.get(uid=campus_uid)
                validated_data['campus'] = campus
            except Campus.DoesNotExist:
                raise serializers.ValidationError({'campus_uid': 'Campus with this UID does not exist.'})
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        campus_uid = validated_data.pop('campus_uid', None)
        if campus_uid:
            try:
                campus = Campus.objects.get(uid=campus_uid)
                instance.campus = campus
            except Campus.DoesNotExist:
                raise serializers.ValidationError({'campus_uid': 'Campus with this UID does not exist.'})
        
        return super().update(instance, validated_data)




class WashingMashineCleanImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashingMashineCleanImage
        fields = ['image']


class WashingMashineSerializer(serializers.ModelSerializer):
    before_and_after_cleaned_image = WashingMashineCleanImageSerializer(many=True, required=False)
    last_cleaned_by_uid = serializers.UUIDField(write_only=True, required=False)
    last_cleaned_by = serializers.SerializerMethodField()  # For read-only field

    class Meta:
        model = WashingMashine
        fields = '__all__'
        extra_kwargs = {
            'last_cleaned_by': {'read_only': True}  # Make sure last_cleaned_by is read-only
        }

    def create(self, validated_data):
        last_cleaned_by_uid = validated_data.pop('last_cleaned_by_uid', None)
        if last_cleaned_by_uid:
            last_cleaned_by = Employee.objects.get(uid=last_cleaned_by_uid)
            validated_data['last_cleaned_by'] = last_cleaned_by
        return super(WashingMashineSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        last_cleaned_by_uid = validated_data.pop('last_cleaned_by_uid', None)
        if last_cleaned_by_uid:
            last_cleaned_by = Employee.objects.get(uid=last_cleaned_by_uid)
            validated_data['last_cleaned_by'] = last_cleaned_by
        return super(WashingMashineSerializer, self).update(instance, validated_data)

    def get_last_cleaned_by(self, obj):
        if obj.last_cleaned_by:
            return obj.last_cleaned_by.uid
        return None

    
class DryingMashineCleanImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryingMashineCleanImage
        fields = ['image']

class DryingMashineSerializer(serializers.ModelSerializer):
    before_and_after_cleaned_image = DryingMashineCleanImageSerializer(many=True, required=False)
    last_cleaned_by_uid = serializers.UUIDField(write_only=True, required=False)
    last_cleaned_by = serializers.SerializerMethodField()  

    class Meta:
        model = DryingMashine
        fields = '__all__'
        extra_kwargs = {
            'last_cleaned_by': {'read_only': True}  
        }

    def create(self, validated_data):
        last_cleaned_by_uid = validated_data.pop('last_cleaned_by_uid', None)
        if last_cleaned_by_uid:
            last_cleaned_by = Employee.objects.get(uid=last_cleaned_by_uid)
            validated_data['last_cleaned_by'] = last_cleaned_by
        return super(DryingMashineSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        last_cleaned_by_uid = validated_data.pop('last_cleaned_by_uid', None)
        if last_cleaned_by_uid:
            last_cleaned_by = Employee.objects.get(uid=last_cleaned_by_uid)
            validated_data['last_cleaned_by'] = last_cleaned_by
        return super(DryingMashineSerializer, self).update(instance, validated_data)

    def get_last_cleaned_by(self, obj):
        if obj.last_cleaned_by:
            return obj.last_cleaned_by.uid
        return None

    

class VehicleExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleExpenses
        fields = "__all__"

class VehicleSerializer(serializers.ModelSerializer):
    last_driver = serializers.SlugRelatedField(
        slug_field='uid',  
        queryset=Employee.objects.all()
    )
    expenses = serializers.SlugRelatedField(
        slug_field='uid',  
        queryset=VehicleExpenses.objects.all()
    )

    class Meta:
        model = Vehicle
        fields = "__all__"

    
    



class FoldingTableSerializer(serializers.ModelSerializer):
    last_used_by = serializers.SlugRelatedField(
        slug_field='uid',  
        queryset=Employee.objects.all()
    )
   

    class Meta:
        model = FoldingTable
        fields = "__all__"


class complaintSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    campus = CampusSerializer(read_only=True)

    # Write-only fields for creating/updating
    employee_uid = serializers.UUIDField(write_only=True)
    campus_uid = serializers.UUIDField(write_only=True)

    class Meta:
        model = complaint
        fields = "__all__"

    def create(self, validated_data):
        employee_uid = validated_data.pop('employee_uid', None)
        campus_uid = validated_data.pop('campus_uid', None)

        # Fetch related instances
        if employee_uid:
            validated_data['employee'] = Employee.objects.get(uid=employee_uid)
        if campus_uid:
            validated_data['campus'] = Campus.objects.get(uid=campus_uid)

        return super().create(validated_data)
    

class DailyImageSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyImageSheet
        fields = "__all__"  
        
class StudentDaySheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDaySheet
        fields = "__all__"  


class FacultyDaySheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyDaySheet
        fields = "__all__"  
    

class StudentRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRemark
        fields = "__all__"  

class RemarkByWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemarkByWarehouse
        fields = "__all__"  

class CollectionSerializer(serializers.ModelSerializer):
    student_day_sheet = StudentDaySheetSerializer(many=True)
    faculty_day_sheet = FacultyDaySheetSerializer(many=True)
    daily_image_sheet = DailyImageSheetSerializer(many=True)
    student_remark = StudentRemarkSerializer(many=True)
    warehouse_remark = RemarkByWarehouseSerializer(many=True)

    class Meta:
        model = Collection
        fields = "__all__"




class EmployeeSignInserializer(serializers.Serializer):
    email= serializers.EmailField()
    password = serializers.CharField(max_length=255)
    