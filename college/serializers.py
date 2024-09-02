from rest_framework import serializers
from college.models import (Employee, EmployeeDailyImage,College,Campus,Faculty,Student,
                            WashingMashine, WashingMashineCleanImage,DryingMashine,DryingMashineCleanImage,
                            VehicleExpenses,Vehicle,FoldingTable,complaint,
                            DailyImageSheet,StudentDaySheet,FacultyDaySheet,
                            StudentRemark,RemarkByWarehouse,Collection,Routes,LogisticBagNumer,FacultybagNumbers,
                            FilldArea,DryArea
                            )
class EmployeeDailyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDailyImage
        fields = ['image']

class EmployeeSerializer(serializers.ModelSerializer):
    daily_images = EmployeeDailyImageSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = ['uid','id','email','name','mobile','dob','profile_image','employee_type','salary','aadhar_number','daily_images','username','is_superuser','last_login']
        extra_kwargs = {"password": {"write_only": True}}





class EmployeeSerializerData(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','uid','name','mobile','profile_image']

class RoutesSerializer(serializers.ModelSerializer):
    employee_uid = serializers.CharField(write_only=True, required=True)
    # employee = EmployeeSerializerData(read_only=True)
    class Meta:
        model = Routes
        fields = '__all__'

    def create(self, validated_data):
        employee_uid = validated_data.pop("employee_uid")
        if employee_uid:
            try:
                employee_instance = Employee.objects.get(uid=employee_uid)
                if employee_instance.employee_type ==  "Driver":
                    validated_data['employee'] = employee_instance
                else:
                    raise serializers.ValidationError({'Error': 'employee type is not a driver'})                    
            except Employee.DoesNotExist:
                raise serializers.ValidationError({'Employee': 'Employee with this UID does not exist.'})
        
        routes = super().create(validated_data)
        return routes
class CollegeSerializer(serializers.ModelSerializer):
    campus_employee = serializers.SlugRelatedField(
        queryset=Employee.objects.all(),
        many=True,
        slug_field='uid'
    )
    route_uid = serializers.CharField(write_only=True, required=True)
    routes = RoutesSerializer(read_only=True)
    

    class Meta:
        model = College
        fields = "__all__"

    def create(self, validated_data):
        # Pop the campus_employee data from validated_data
        employees_data = validated_data.pop('campus_employee', [])
        routes_uid = validated_data.pop("route_uid")
        if routes_uid:
            try:
                routes_instance = Routes.objects.get(uid=routes_uid)
                validated_data['routes'] = routes_instance
            except Routes.DoesNotExist:
                raise serializers.ValidationError({'Routes': 'Routes with this UID does not exist.'})
        college = College.objects.create(**validated_data)
        # Set the campus_employee relationships
        college.campus_employee.set(employees_data) 
        return college
    
    def update(self, instance, validated_data):
    # Handle route update
        routes_uid = validated_data.pop("route_uid", None)
        if routes_uid:
            try:
                routes_instance = Routes.objects.get(uid=routes_uid)
                instance.routes = routes_instance
            except Routes.DoesNotExist:
                raise serializers.ValidationError({'Routes': 'Routes with this UID does not exist.'})

        # Handle campus_employee update
        if 'campus_employee' in validated_data:
            employees_data = validated_data.pop('campus_employee')
            instance.campus_employee.set(employees_data)

        # Update the remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    


        
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


class GetCampusSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Campus
        fields = '__all__'

class FacultySerializer(serializers.ModelSerializer):
    campus_uid = serializers.CharField(write_only=True, required=False)
    campus = serializers.SlugRelatedField(
        queryset=Campus.objects.all(),
        slug_field='uid',
        required=False
    )

    class Meta:
        model = Faculty
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
    
class EmployeeSignInserializer(serializers.Serializer):
    email= serializers.EmailField()
    password = serializers.CharField(max_length=255)

class DailyImageSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyImageSheet
        fields = ['image']

class StudentDaySheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDaySheet
        fields =  "__all__"

class FacultyDaySheetSerializer(serializers.ModelSerializer):
    faculty = serializers.SlugRelatedField(slug_field='uid', queryset=Faculty.objects.all())

    class Meta:
        model = FacultyDaySheet
        fields = "__all__"


class StudentRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRemark
        fields = "__all__"

class RemarkByWarehouseSerializer(serializers.ModelSerializer):
    employee_uid = serializers.CharField(write_only=True, required=False)
    employee = serializers.SlugRelatedField(
        queryset=Employee.objects.all(),
        slug_field='uid'
    )

    class Meta:
        model = RemarkByWarehouse
        fields = '__all__'

    def create(self, validated_data):
        employee_uid = validated_data.pop('employee_uid', None)
        if employee_uid:
            try:
                employee = Employee.objects.get(uid=employee_uid)
                validated_data['employee'] = employee
            except Employee.DoesNotExist:
                raise serializers.ValidationError({'employee_uid': 'Employee with this UID does not exist.'})
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        employee_uid = validated_data.pop('employee_uid', None)
        if employee_uid:
            try:
                employee = Employee.objects.get(uid=employee_uid)
                instance.employee = employee
            except Employee.DoesNotExist:
                raise serializers.ValidationError({'employee': 'Employee with this UID does not exist.'})
        
        return super().update(instance, validated_data)


class LogisticbagNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticBagNumer
        fields = "__all__"

class FacultybagNumbersSerializer(serializers.ModelSerializer):
    faculty = serializers.SlugRelatedField(slug_field='uid', queryset=Faculty.objects.all())

    class Meta:
        model = FacultybagNumbers
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):

    student_day_sheet = StudentDaySheetSerializer(many=True, required=False)
    faculty_day_sheet = FacultyDaySheetSerializer(many=True, required=False)
    student_remark = StudentRemarkSerializer(many=True, required=False)
    warehouse_remark = RemarkByWarehouseSerializer(many=True, required=False)
    daily_image_sheet = DailyImageSheetSerializer(many=True, required=False)
    campus_pickup_bag_numbers = LogisticbagNumberSerializer(many=True, required=False)
    campus_drop_bag_numbers = LogisticbagNumberSerializer(many=True, required=False)
    warehouse_pickup_bag_numbers = LogisticbagNumberSerializer(many=True, required=False)
    warehouse_drop_bag_numbers = LogisticbagNumberSerializer(many=True, required=False)

    campus_pickup_faculty_bag_number = FacultybagNumbersSerializer(many=True, required=False)
    campus_drop_faculty_bag_number = FacultybagNumbersSerializer(many=True, required=False)
    warehouse_pickup_faculty_bag_number = FacultybagNumbersSerializer(many=True, required=False)
    warehouse_drop_faculty_bag_number = FacultybagNumbersSerializer(many=True, required=False)


 

    campus = CampusSerializer(read_only = True)
    supervisor = EmployeeSerializer(read_only =True)
    pickup_driver = EmployeeSerializer(read_only =True)
    washing_supervisor = EmployeeSerializer(read_only =True)
    drying_supervisor = EmployeeSerializer(read_only =True)
    segregation_supervisor = EmployeeSerializer(read_only =True)
    college_supervisor = EmployeeSerializer(read_only =True)

   

    class Meta:
        model = Collection
        fields = "__all__"

    
        

class CollectionTaskSerializer(serializers.Serializer):
    current_status = serializers.CharField(required=True)



class FilldAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilldArea
        fields = "__all__"


class DryAreaSerializer(serializers.ModelSerializer):
    fill_area = FilldAreaSerializer( required=False)  # Nested serializer for fill_area

    class Meta:
        model = DryArea
        fields = "__all__"

    def create(self, validated_data):
        fill_area_data = validated_data.pop('fill_area', None)
        dry_area = DryArea.objects.create(**validated_data)
        
        if fill_area_data:
            campus_id = fill_area_data.get('campus')
            filled = fill_area_data.get('filled')
            campus = Campus.objects.get(id=campus_id)  # Assuming campus_id is a primary key, adjust as necessary
            FilldArea.objects.create(campus=campus, filled=filled)
            
        return dry_area

   



class CollectionResponseSerializer(serializers.ModelSerializer):

    student_day_sheet = StudentDaySheetSerializer(many=True, required=False)
    faculty_day_sheet = FacultyDaySheetSerializer(many=True, required=False)
    student_remark = StudentRemarkSerializer(many=True, required=False)
    warehouse_remark = RemarkByWarehouseSerializer(many=True, required=False)
    campus_pickup_bag_numbers = LogisticbagNumberSerializer(many=True, required=False)
    campus_drop_bag_numbers = LogisticbagNumberSerializer(many=True, required=False)
    warehouse_pickup_bag_numbers = LogisticbagNumberSerializer(many=True, required=False)
    warehouse_drop_bag_numbers = LogisticbagNumberSerializer(many=True, required=False)

    campus_pickup_faculty_bag_number = FacultybagNumbersSerializer(many=True, required=False)
    campus_drop_faculty_bag_number = FacultybagNumbersSerializer(many=True, required=False)
    warehouse_pickup_faculty_bag_number = FacultybagNumbersSerializer(many=True, required=False)
    warehouse_drop_faculty_bag_number = FacultybagNumbersSerializer(many=True, required=False)


 

    campus = CampusSerializer(read_only = True)
    supervisor = EmployeeSerializer(read_only =True)
    pickup_driver = EmployeeSerializer(read_only =True)
    washing_supervisor = EmployeeSerializer(read_only =True)
    drying_supervisor = EmployeeSerializer(read_only =True)
    segregation_supervisor = EmployeeSerializer(read_only =True)

   

    class Meta:
        model = Collection
        fields = [
            'uid',
            'id',  # or list all fields you want to include
            'campus',
            'student_day_sheet',
            'faculty_day_sheet',
            'total_cloths',
            'total_uniforms',
            'supervisor',
            'pickup_driver',
            'drop_driver',
            'washing_supervisor',
            'drying_supervisor',
            'segregation_supervisor',
            'current_status',
            'ETA',
            'student_remark',
            'warehouse_remark',
            'campus_pickup_bag_numbers',
            'campus_drop_bag_numbers',
            'warehouse_pickup_bag_numbers',
            'warehouse_drop_bag_numbers',
            'campus_pickup_faculty_bag_number',
            'campus_drop_faculty_bag_number',
            'warehouse_pickup_faculty_bag_number',
            'warehouse_drop_faculty_bag_number',
        ]