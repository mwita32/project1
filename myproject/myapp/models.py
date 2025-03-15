from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Allow blank username initially
    reg_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=191, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=255, default="")
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True, auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.username:  # Set username if not provided
            self.username = self.reg_number  # Use reg number as username
        if self.is_admin:
            self.is_superuser = True
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
class County(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SubCounty(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PersonalDetails(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    STUDENT_STATUS_CHOICES = [('KUCCPS', 'Government Sponsored (KUCCPS)'), ('PSSP', 'Self Sponsored (PSSP)')]
    RESIDENTIAL_STATUS_CHOICES = [('Resident', 'Resident'), ('Non Resident', 'Non Resident')]

    name = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=50, unique=True)
    school = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    home_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True)
    next_of_kin = models.CharField(max_length=100)
    next_of_kin_address = models.CharField(max_length=255)
    next_of_kin_phone = models.CharField(max_length=15)
    chief_name = models.CharField(max_length=100)
    chief_address = models.CharField(max_length=255)
    chief_phone = models.CharField(max_length=15)
    disability = models.BooleanField(default=False)
    disability_details = models.CharField(max_length=255, blank=True, null=True)
    student_status = models.CharField(max_length=10, choices=STUDENT_STATUS_CHOICES)
    residential_status = models.CharField(max_length=15, choices=RESIDENTIAL_STATUS_CHOICES)

    def __str__(self):
        return self.name

class FamilyBackground(models.Model):
    parental_status = models.CharField(max_length=10, choices=[
        ("both", "Have both parents"),
        ("one", "Have one parent"),
        ("orphan", "Total orphan"),
    ])
    death_certificate = models.FileField(upload_to="documents/", null=True, blank=True)
    father_age = models.IntegerField(null=True, blank=True)
    father_occupation = models.CharField(max_length=100, null=True, blank=True)
    father_employer = models.CharField(max_length=100, null=True, blank=True)
    father_health_status = models.FileField(upload_to="documents/", null=True, blank=True)
    mother_age = models.IntegerField(null=True, blank=True)
    mother_occupation = models.CharField(max_length=100, null=True, blank=True)
    mother_employer = models.CharField(max_length=100, null=True, blank=True)
    mother_health_status = models.FileField(upload_to="documents/", null=True, blank=True)
    total_siblings = models.IntegerField()
    university_siblings = models.IntegerField(null=True, blank=True)
    secondary_siblings = models.IntegerField(null=True, blank=True)
    out_of_school_siblings = models.IntegerField(null=True, blank=True)
    out_of_school_reason = models.TextField(null=True, blank=True)
    working_siblings_occupation = models.TextField(null=True, blank=True)