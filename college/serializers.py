from rest_framework import serializers
from college.models import (Employee, EmployeeDailyImage,College,Campus,Faculty,Student,
                            WashingMashine, WashingMashineCleanImage,DryingMashine,DryingMashineCleanImage,
                            VehicleExpenses,Vehicle,FoldingTable,complaint
                            )

class EmployeeDailyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDailyImage
        fields = ['image']

class EmployeeSerializer(serializers.ModelSerializer):
    daily_images = EmployeeDailyImageSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = '__all__'





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
        employees_data = validated_data.pop('campus_employee')
        college = College.objects.create(**validated_data)
        college.campus_employee.set(employees_data)  # Associate employees by UID
        return college
    



class CampusSerializer(serializers.ModelSerializer):
    college_uid = serializers.CharField(write_only=True, required=False)
    college = serializers.SlugRelatedField(slug_field='uid', queryset=College.objects.all())

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
    employee = serializers.SlugRelatedField(
        slug_field='uid',  
        queryset=Employee.objects.all()
    )
   
    campus = serializers.SlugRelatedField(
        slug_field='uid',  
        queryset=Campus.objects.all()
    )
    class Meta:
        model = complaint
        fields = "__all__"