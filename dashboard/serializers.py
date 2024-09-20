from college.models import *
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['uid','name']

class RoutesSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True,many=False)

    class Meta:
        model = Routes
        fields = ['uid','name',"employee"]


class CollegeDetailsSerializer(serializers.ModelSerializer):
    campus_employee = EmployeeSerializer(many=True, required=False)
    routes = RoutesSerializer(read_only =True)
    class Meta:
        model = College
        fields = "__all__"
    

class CollegeDashboardSerializer(serializers.ModelSerializer):
    campus_employee = serializers.SlugRelatedField(
        queryset=Employee.objects.all(),
        many=True,
        slug_field='uid'
    )
    
    # Nested route creation
    routes = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = College
        fields = "__all__"

    def create(self, validated_data):
        # Pop the campus_employee and routes data
        employees_data = validated_data.pop('campus_employee', [])
        route_data = validated_data.pop('routes', None)

        # Handle route creation if route data is provided
        if route_data:
            try:
                route_employee = Employee.objects.get(uid=route_data['employee_uid'])
                routes_instance = Routes.objects.create(
                    name=route_data['name'],
                    employee=route_employee
                )
                validated_data['routes'] = routes_instance
            except Employee.DoesNotExist:
                raise serializers.ValidationError({'routes': 'Employee with this UID does not exist.'})

        # Create the College instance
        college = College.objects.create(**validated_data)

        # Set the campus_employee relationships if employees are provided
        if employees_data:
            college.campus_employee.set(employees_data)

        return college


    





class CampusDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = "__all__"

class facultyDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ["uid","id",'name']
    


class EmployeeDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class CampusDashboard2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ["uid",'name']

class EmployeeDashboard2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["uid",'name']

class CollectionDashboardSerializer(serializers.ModelSerializer):
    campus = CampusDashboard2Serializer(read_only = True)
    supervisor = EmployeeDashboard2Serializer(read_only =True)
    class Meta:
        model = Collection
        fields = ["id",'uid','campus','total_cloths','total_uniforms',"supervisor",'ETA','isActive']



class RouteDashboardSerializer(serializers.ModelSerializer):
    employee = EmployeeDashboard2Serializer(read_only =True)
    class Meta:
        model= Routes
        fields = "__all__"