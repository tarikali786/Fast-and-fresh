from django.db import models
from django.utils import timezone
from datetime import timedelta
from core.behaviours import StatusMixin, UUIDMixin
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

def upload_location(instance, filename):
    ext_set = filename.split(".")
    model = instance.__class__.__name__.lower()
    return f"{model}/{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext_set[-1]}"




# Models
class College(StatusMixin):
    name = models.CharField(max_length=300,  blank=True,null=True)
    monthly_payment =  models.CharField(max_length=300,  blank=True,null=True)
    delivery_time = models.TimeField( blank=True,null=True)
    schedule = models.IntegerField( blank=True,null=True)
    campus_employee = models.ManyToManyField("Employee", blank=True)
    routes = models.ForeignKey('Routes',on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name

class Campus(StatusMixin):
    tag_name = models.CharField(max_length=100,  blank=True,null=True)
    name = models.CharField(max_length=255,  blank=True,null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='campuses',null=True,blank=True)
    uniform = models.BooleanField(default=False,null=True, blank=True )
    max_student_count = models.IntegerField(default=0,null=True,blank=True)
    def __str__(self):
        return f"{self.name} "

class Faculty(StatusMixin):
    name = models.CharField(max_length=300,  blank=True,null=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE,  blank=True, null=True ,related_name='faculties')

    def __str__(self):
        return self.name.capitalize()

class Student(StatusMixin):
    name = models.CharField(max_length=300,  blank=True,null=True)
    tag_number = models.CharField(max_length=20,  blank=True,null=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE,  blank=True,null=True, related_name='students')
    mobile = models.BigIntegerField(default=0,  blank=True,null=True)
    email = models.EmailField( unique=True, blank=True,null=True)
    dob = models.DateField( blank=True,null=True)
    year = models.DateField( blank=True)
    branch = models.CharField(max_length=300,  blank=True,null=True)

    

    def __str__(self):
        return self.name.capitalize()

class EmployeeDailyImage(UUIDMixin):
    image = models.ImageField(upload_to=upload_location)

    def __str__(self):
        return f"Image {self.id}"
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
class Employee(AbstractUser):
    EMPLOYEE_TYPE_CHOICES = [
        ("Admin", "Admin"),
        ("Campus_Employee", "Campus_Employee"),
        ("Driver", "Driver"),
        ("Washing", "Washing"),
        ("Drying", "Drying"),
        ("Segregation", "Segregation"),
    ]
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField( unique=True, blank=True, null=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    mobile = models.BigIntegerField(default=0, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPE_CHOICES, blank=True, null=True)
    salary = models.IntegerField(default=0, blank=True)
    aadhar_number = models.BigIntegerField(blank=True, null=True, default=0)
    daily_images = models.ManyToManyField(EmployeeDailyImage, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)
        self.limit_daily_images()

    def limit_daily_images(self):
        if self.daily_images.count() > 30:
            excess_images = self.daily_images.all()[0:self.daily_images.count() - 30]
            for image in excess_images:
                self.daily_images.remove(image)
                image.image.delete(save=False)
                image.delete()

    def __str__(self) -> str:
        return self.email
class DailyImageSheet(UUIDMixin):
    image = models.ImageField(upload_to=upload_location,  blank=True,null=True)

class StudentDaySheet(UUIDMixin):
    tag_number = models.CharField(max_length=20,  blank=True,null=True)
    campus_regular_cloths = models.IntegerField( blank=True,null=True ,default=0)
    campus_uniforms = models.IntegerField( blank=True,null=True, default=0)
    ware_house_regular_cloths =models.IntegerField( blank=True,null=True, default=0)
    ware_house_uniform =models.IntegerField( blank=True,null=True, default=0)
    delivered = models.BooleanField(default=False,null=True,blank=True)
    def __str__(self) -> str:
        return self.tag_number

class FacultyDaySheet(UUIDMixin):
    # changes
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True,blank=True)
    regular_cloths = models.IntegerField( blank=True,null=True, default=0)
    ware_house_regular_cloths =models.IntegerField( blank=True,null=True, default=0)
    delivered = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self) -> str:
        return self.tag_number

class StudentRemark(UUIDMixin):
    tag_number = models.CharField(max_length=20,  blank=True,null=True)
    remark = models.TextField(blank=True,null=True)
    remark_type = models.CharField(max_length=250,null=True,blank=True)
    remark_status = models.BooleanField(default=False,null=True,blank=True)
    resolution = models.CharField(max_length=250,null=True,blank=True)
    


    def __str__(self) -> str:
        return self.tag_number

class RemarkByWarehouse(UUIDMixin):
    tag_number = models.CharField(max_length=20,  blank=True,null=True)
    remark = models.TextField(blank=True,null=True)
    employee = models.ForeignKey(Employee,blank=True,null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.tag_number

class LogisticBagNumer(models.Model):
    bag_number = models.IntegerField(  blank=True,null=True)

class FacultybagNumbers(models.Model):
    number_of_bag = models.IntegerField(null=True,blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE,null=True,blank=True)
    photo = models.ImageField(upload_to=upload_location,  blank=True,null=True)

class OtherClothBagNumber(models.Model):
    number_of_bag = models.IntegerField(null=True,blank=True)
    photo = models.ImageField(upload_to=upload_location,  blank=True,null=True)

class PreviousStatus(models.Model):
    status = models.CharField(max_length=100, blank=True, null=True)
    updated_time = models.DateTimeField(null=True,blank=True)

class OtherclothDaySheet(UUIDMixin):
    name = models.CharField(max_length=200 , null=True,blank=True )
    number_of_items = models.IntegerField(default=0,null=True,blank=True)
    delivered = models.BooleanField(default=False,null=True,blank=True)



class Collection(StatusMixin):
    CollectionStatus =[
        ("READY_TO_PICK","READY_TO_PICK"),
        ("INTRANSIT_FROM_cAMPUS","INTRANSIT_FROM_cAMPUS"),
        ("DELIVERED_TO_WAREHOUSE","DELIVERED_TO_WAREHOUSE"),
        ("WASHING","WASHING"),
        ("WASHING_DONE","WASHING_DONE"),
        ("DRYING","DRYING"),
        ("DRYING_DONE","DRYING_DONE"),
        ("IN_SEGREGATION","IN_SEGREGATION"),
        ("READY_FOR_DELIVERY","READY_FOR_DELIVERY"),
        ("INTRANSIT_FROM_WAREHOUSE","INTRANSIT_FROM_WAREHOUSE"),
        ("DELIVERED_TO_CAMPUS","DELIVERED_TO_CAMPUS"),
        ("DELIVERED_TO_STUDENT","DELIVERED_TO_STUDENT"),
    ]
#    changes
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE,  blank=True,null=True)
    student_day_sheet = models.ManyToManyField(StudentDaySheet, blank=True)
    faculty_day_sheet = models.ManyToManyField(FacultyDaySheet, blank=True)
    total_cloths = models.IntegerField( blank=True,null=True, default=0)
    total_uniforms = models.IntegerField( blank=True,null=True, default=0)
    supervisor = models.ForeignKey(Employee,  blank=True,null=True, on_delete=models.CASCADE, related_name='collections')
    daily_image_sheet = models.ManyToManyField(DailyImageSheet, blank=True)
    pickup_driver = models.ForeignKey(Employee,  blank=True,null=True ,on_delete=models.CASCADE, related_name='pickup_collections')
    campus_pickup_collection_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    campus_drop_collection_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    warehouse_pickup_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    warehouse_drop_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    washing_supervisor = models.ForeignKey(Employee,  blank=True,null=True ,on_delete=models.CASCADE, related_name='washing_supervisions')
    drying_supervisor = models.ForeignKey(Employee,  blank=True,null=True, on_delete=models.CASCADE, related_name='drying_supervisions')
    segregation_supervisor = models.ForeignKey(Employee,  blank=True,null=True, on_delete=models.CASCADE, related_name='segregation_supervisions')
    drop_driver = models.ForeignKey(Employee,  blank=True,null=True,on_delete=models.CASCADE, related_name='drop_drivers')
    # college_supervisor = models.ForeignKey(Employee,  blank=True,null=True, on_delete=models.CASCADE, related_name='college_supervisions')
    current_status = models.CharField(max_length=100, choices=CollectionStatus, blank=True,null=True )
    ETA = models.IntegerField(  blank=True,null=True)  #fatch college shcedule
    student_remark = models.ManyToManyField(StudentRemark,blank=True)
    warehouse_remark = models.ManyToManyField(RemarkByWarehouse,blank=True)

    # new added
    campus_pickup_bag_numbers = models.ManyToManyField(LogisticBagNumer,blank=True,  related_name='campus_pickup_collections'    )
    campus_drop_bag_numbers = models.ManyToManyField(LogisticBagNumer, blank=True, related_name='campus_drop_collections'    )
    warehouse_pickup_bag_numbers = models.ManyToManyField(LogisticBagNumer, blank=True,related_name='warehouse_pickup_collections'    )
    warehouse_drop_bag_numbers = models.ManyToManyField(LogisticBagNumer, blank=True, related_name='warehouse_drop_collections')
    campus_pickup_faculty_bag_number = models.ManyToManyField(FacultybagNumbers, blank=True,related_name='campus_pickup_faculty_collections' )
    campus_drop_faculty_bag_number = models.ManyToManyField(FacultybagNumbers,blank=True,related_name='campus_drop_faculty_collections')
    warehouse_pickup_faculty_bag_number = models.ManyToManyField(FacultybagNumbers,blank=True,related_name='warehouse_pickup_faculty_collections'    )
    warehouse_drop_faculty_bag_number = models.ManyToManyField(FacultybagNumbers,blank=True,related_name='warehouse_drop_faculty_collections')
    previous_status = models.ManyToManyField(PreviousStatus,blank=True)

    # new
    no_tag = models.IntegerField(null=True,blank=True,default=0)
    other_cloth_daysheet = models.ManyToManyField(OtherclothDaySheet,blank=True)
    other_cloth_campus_pickup =  models.ManyToManyField(OtherClothBagNumber,blank=True,related_name='campus_pickup_otherCloth_collections'    )
    other_cloth_campus_drop =  models.ManyToManyField(OtherClothBagNumber,blank=True,related_name='campus_drop_otherCloth_collections'    )
    other_cloth_warehouse_pickup =  models.ManyToManyField(OtherClothBagNumber,blank=True,related_name='warehouse_pickup_otherCloth_collections'    )
    other_cloth_warehouse_drop =  models.ManyToManyField(OtherClothBagNumber,blank=True,related_name='warehouse_drop_otherCloth_collections'    )
    completed_segregation_range = models.JSONField(null=True, blank=True)
    




    

    def __str__(self):
        return f"Collection {self.id} - {self.current_status}"

class WashingMashineCleanImage(UUIDMixin):
    image = models.ImageField(upload_to=upload_location,  blank=True,null=True)

    def __str__(self):
        return f"Image {self.id} - {self.image.name}"

class WashingMashine(StatusMixin):
    Mashing_status = [
    ("NOT_IN_USE", "Not in Use"),
    ("Working", "Working"),
        ]
    mashine_number = models.CharField(max_length=100,  blank=True,null=True)
    last_cleaned_date = models.DateField( blank=True)
    last_cleaned_by = models.ForeignKey('Employee', on_delete=models.CASCADE,  blank=True,null=True)
    status = models.CharField(max_length=100, choices=Mashing_status,  blank=True,null=True)
    before_and_after_cleaned_image = models.ManyToManyField(WashingMashineCleanImage, blank=True)

    def save(self, *args, **kwargs):
        super(WashingMashine, self).save(*args, **kwargs)
        self.limit_cleaning_images()

    def limit_cleaning_images(self):
        # Get the cutoff date (30 days ago)
        cutoff_date = timezone.now() - timedelta(days=30)
        # Filter images older than 30 days and delete them
        old_images = self.before_and_after_cleaned_image.filter(created_at__lt=cutoff_date)
        for image in old_images:
            # Remove the image from the ManyToMany field
            self.before_and_after_cleaned_image.remove(image)
            # Delete the image file from storage
            image.image.delete(save=False)
            # Delete the image record from the database
            image.delete()

    def __str__(self):
        return f"Washing Machine {self.mashine_number}"

class DryingMashineCleanImage(UUIDMixin):
    image = models.ImageField(upload_to=upload_location,  blank=True,null=True)

class DryingMashine(StatusMixin):
    Mashing_status = [
    ("NOT_IN_USE", "Not in Use"),
    ("Working", "Working"),
        ]
    mashine_number = models.CharField(max_length=100,  blank=True,null=True)
    last_cleaned_date = models.DateField( blank=True,null=True)
    last_cleaned_by = models.ForeignKey('Employee', on_delete=models.CASCADE,  blank=True,null=True)
    status = models.CharField(max_length=100, choices=Mashing_status,  blank=True,null=True)
    before_and_after_cleaned_image = models.ManyToManyField(DryingMashineCleanImage, blank=True)

    def save(self, *args, **kwargs):
        super(DryingMashine, self).save(*args, **kwargs)
        self.limit_cleaning_images()

    def limit_cleaning_images(self):
        # Get the cutoff date (30 days ago)
        cutoff_date = timezone.now() - timedelta(days=30)
        # Filter images older than 30 days and delete them
        old_images = self.before_and_after_cleaned_image.filter(created_at__lt=cutoff_date)
        for image in old_images:
            # Remove the image from the ManyToMany field
            self.before_and_after_cleaned_image.remove(image)
            # Delete the image file from storage
            image.image.delete(save=False)
            # Delete the image record from the database
            image.delete()

    def __str__(self):
        return f"Drying Machine {self.mashine_number}"
    
class VehicleExpenses(UUIDMixin):
    expense_type = models.CharField(blank=True,null=True, max_length=200)
    amount = models.IntegerField(default=0,blank=True,null=True)
    expense_date = models.DateField(blank=True,null=True)
    image = models.ImageField(upload_to=upload_location,  blank=True,null=True)

    def __str__(self) -> str:
        return self.expense_type

class Vehicle(StatusMixin):
    name = models.CharField(max_length=200,  blank=True,null=True)
    make = models.CharField(max_length=200,  blank=True,null=True)
    number_plate = models.CharField(max_length=200,  blank=True,null=True)
    odo_meter = models.IntegerField(default=0,  blank=True,null=True)
    odo_meter_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    spare_tyre = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    front_side = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    left_side = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    right_side = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    back_side = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    last_driver = models.ForeignKey(Employee, on_delete=models.CASCADE,  blank=True,null=True)
    fuel_level = models.IntegerField( blank=True,null=True )
    expenses = models.ForeignKey(VehicleExpenses,on_delete=models.CASCADE,blank=True,null=True, related_name="vehicle")
    def __str__(self):
        return f"{self.name} ({self.number_plate})"





class FoldingTable(StatusMixin):
    table_number = models.CharField(max_length=200,  blank=True,null=True)
    last_used_by = models.ForeignKey(Employee, on_delete=models.CASCADE,  blank=True,null=True)


    def __str__(self):
        return self.table_number



class complaint(UUIDMixin):
    campus = models.ForeignKey(Campus,on_delete=models.CASCADE,blank=True)
    complaint = models.TextField(blank=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,blank=True)


    def __str__(self) -> str:
        return self.campus
    



class Routes(StatusMixin):
    name = models.CharField(max_length=200,  blank=True,null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True,blank=True,related_name="routes_employee")




class FilldArea(models.Model):
    campus = models.ForeignKey(Campus,on_delete=models.CASCADE,null=True,blank=True)
    filled = models.JSONField(null=True,blank=True)


class DryArea(StatusMixin):
    dry_area_id = models.IntegerField(blank=True)
    row = models.IntegerField(blank=True)
    column = models.IntegerField(blank=True)
    fill_area = models.ForeignKey(FilldArea,on_delete=models.CASCADE,null=True,blank=True)


