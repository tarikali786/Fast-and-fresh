from django.db import models
from django.utils import timezone
from datetime import timedelta
from core.behaviours import StatusMixin, UUIDMixin

def upload_location(instance, filename):
    ext_set = filename.split(".")
    model = instance.__class__.__name__.lower()
    return f"{model}/{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext_set[-1]}"



class CollectionStatus(models.TextChoices):
    READY_TO_PICK = '0', "Ready to Pick"
    IN_TRANSIT = '1', "In Transit"
    WASHING = '2', "Washing"
    WASHING_DONE = '3', "Washing done"
    DRYING = '4', "Drying"
    DRYING_DONE = '5', "Drying done"
    IN_SEGREGATION = '6', "In Segregation"
    SEGREGATION_DONE = '7', "Segregation done"
    READY_FOR_DELIVERY = '8', "Ready for Delivery"
    DELIVERED_TO_CAMPUS = '9', "Delivered to campus"
    DELIVERED_TO_STUDENT = '10', 'Delivered to student'

class MashineStatus(models.TextChoices):
    NOT_IN_USE = '0', "Not In use"
    WORKING = '1', "Working"

# Models
class College(StatusMixin):
    name = models.CharField(max_length=300,  blank=True,null=True)
    monthly_payment =  models.CharField(max_length=300,  blank=True,null=True)
    delivery_time = models.TimeField( blank=True,null=True)
    schedule = models.IntegerField( blank=True,null=True)
    campus_employee = models.ManyToManyField("Employee", blank=True)

    def __str__(self):
        return self.name

class Campus(StatusMixin):
    tag_name = models.CharField(max_length=100,  blank=True,null=True)
    name = models.CharField(max_length=255,  blank=True,null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='campuses',null=True,blank=True)

    def __str__(self):
        return f"{self.name} "

class Faculty(StatusMixin):
    name = models.CharField(max_length=300,  blank=True,null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE,  blank=True, null=True ,related_name='faculties')

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

    def save(self, *args, **kwargs):
        if self.campus:
            if not self.tag_number:
                campus_tag_name = self.campus.tag_name
                student_count = Student.objects.filter(campus=self.campus).count() + 1
                self.tag_number = f"{campus_tag_name}{student_count:03d}"
        
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.name.capitalize()

class EmployeeDailyImage(UUIDMixin):
    image = models.ImageField(upload_to=upload_location)

    def __str__(self):
        return f"Image {self.id}"

class Employee(StatusMixin):
    EMPLOYEE_TYPE_CHOICES = [
        ("Admin", "Admin"),
        ("Campus_Employee", "Campus Employee"),
        ("Driver", "Driver"),
        ("Washing", "Washing"),
        ("Drying", "Drying"),
        ("Segregation", "Segregation"),
    ]
    name = models.CharField(max_length=300,  blank=True,null=True)
    mobile = models.BigIntegerField(default=0,  blank=True,null=True)
    dob = models.DateField( blank=True,null=True)
    profile_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPE_CHOICES,  blank=True,null=True)
    salary = models.IntegerField(default=0,  blank=True)
    aadhar_number = models.BigIntegerField( blank=True,null=True ,default=0)
    daily_images = models.ManyToManyField(EmployeeDailyImage, blank=True)

    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)
        self.limit_daily_images()

    def limit_daily_images(self):
        if self.daily_images.count() > 30:
            excess_images = self.daily_images.all()[0:self.daily_images.count() - 30]
            for image in excess_images:
                # Remove the image from the ManyToMany field
                self.daily_images.remove(image)
                # Delete the image file from storage
                image.image.delete(save=False)
                # Delete the image record from the database
                image.delete()

    def __str__(self) -> str:
        return self.name

class DailyImageSheet(UUIDMixin):
    image = models.ImageField(upload_to=upload_location,  blank=True,null=True)

class StudentDaySheet(UUIDMixin):
    tag_number = models.CharField(max_length=20,  blank=True,null=True)
    regular_cloths = models.IntegerField( blank=True,null=True ,default=0)
    uniforms = models.IntegerField( blank=True,null=True, default=0)

    def __str__(self) -> str:
        return self.tag_number

class FacultyDaySheet(UUIDMixin):
    tag_number = models.CharField(max_length=20,  blank=True,null=True)
    regular_cloths = models.IntegerField( blank=True,null=True, default=0)

    def __str__(self) -> str:
        return self.tag_number

class StudentRemark(models.Model):
    tag_number = models.CharField(max_length=20,  blank=True,null=True)
    remark = models.TextField(blank=True,null=True)

    def __str__(self) -> str:
        return self.tag_number

class RemarkByWarehouse(models.Model):
    tag_number = models.CharField(max_length=20,  blank=True,null=True)
    remark = models.TextField(blank=True,null=True)
    employee = models.ForeignKey(Employee,blank=True,null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.tag_number


class Collection(StatusMixin):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE,  blank=True,null=True)
    student_day_sheet = models.ManyToManyField(StudentDaySheet, blank=True)
    faculty_day_sheet = models.ManyToManyField(FacultyDaySheet, blank=True)
    total_cloths = models.IntegerField( blank=True,null=True, default=0)
    total_uniforms = models.IntegerField( blank=True,null=True, default=0)
    supervisor = models.ForeignKey(Employee,  blank=True,null=True, on_delete=models.CASCADE, related_name='collections')
    daily_image_sheet = models.ManyToManyField(DailyImageSheet, blank=True)
    pickup_driver = models.ForeignKey(Employee,  blank=True,null=True ,on_delete=models.CASCADE, related_name='pickup_collections')
    pickup_collection_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    collection_in_truck_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    collection_in_warehouse_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    faculty_cloths_in_campus_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    faculty_cloths_in_warehouse_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    collection_while_dropping_in_truck = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    drop_in_campus_image = models.ImageField(upload_to=upload_location,  blank=True,null=True)
    washing_supervisor = models.ForeignKey(Employee,  blank=True,null=True ,on_delete=models.CASCADE, related_name='washing_supervisions')
    drying_supervisor = models.ForeignKey(Employee,  blank=True,null=True, on_delete=models.CASCADE, related_name='drying_supervisions')
    segregation_supervisor = models.ForeignKey(Employee,  blank=True,null=True, on_delete=models.CASCADE, related_name='segregation_supervisions')
    drop_driver = models.ForeignKey(Employee,  blank=True,null=True,on_delete=models.CASCADE, related_name='drop_drivers')
    college_supervisor = models.ForeignKey(Employee,  blank=True,null=True, on_delete=models.CASCADE, related_name='college_supervisions')
    current_status = models.CharField(max_length=100, choices=CollectionStatus.choices, blank=True,null=True )
    ETA = models.IntegerField(  blank=True,null=True)  #fatch college shcedule
    student_remark = models.ManyToManyField(StudentRemark,blank=True)
    warehouse_remark = models.ManyToManyField(RemarkByWarehouse,blank=True)


    def save(self, *args, **kwargs):
        # Calculate total_cloths
        self.total_cloths = sum(
            student_sheet.regular_cloths for student_sheet in self.student_day_sheet.all()
        ) + sum(
            faculty_sheet.regular_cloths for faculty_sheet in self.faculty_day_sheet.all()
        )

        # Calculate total_uniforms
        self.total_uniforms = sum(
            student_sheet.uniforms for student_sheet in self.student_day_sheet.all()
        ) + sum(
            faculty_sheet.uniforms for faculty_sheet in self.faculty_day_sheet.all()
        )

        # Save the instance
        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return f"Collection {self.id} - {self.current_status}"

class WashingMashineCleanImage(UUIDMixin):
    image = models.ImageField(upload_to=upload_location,  blank=True,null=True)

    def __str__(self):
        return f"Image {self.id} - {self.image.name}"

class WashingMashine(StatusMixin):
    mashine_number = models.CharField(max_length=100,  blank=True,null=True)
    last_cleaned_date = models.DateField( blank=True)
    last_cleaned_by = models.ForeignKey('Employee', on_delete=models.CASCADE,  blank=True,null=True)
    status = models.CharField(max_length=100, choices=MashineStatus.choices,  blank=True,null=True)
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
    mashine_number = models.CharField(max_length=100,  blank=True,null=True)
    last_cleaned_date = models.DateField( blank=True,null=True)
    last_cleaned_by = models.ForeignKey('Employee', on_delete=models.CASCADE,  blank=True,null=True)
    status = models.CharField(max_length=100, choices=MashineStatus.choices,  blank=True,null=True)
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