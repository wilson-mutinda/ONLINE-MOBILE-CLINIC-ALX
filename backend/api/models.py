from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required!")
        
        email = self.normalize_email(email)
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("date_joined", timezone.now())  # Add this line
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(email, password, **extra_fields)
    
# role model
class Role(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Custom user model 
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user', null=True)  # Changed from string to ID

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.email

# Patient model   
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient')
    phone = models.CharField(max_length=10, unique=True)
    date_of_birth = models.DateField()
    address = models.TextField()

    def __str__(self):
        return f'{self.user.username} ({self.phone})'

# Specialization model   
class Specialization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Specialist model   
class Specialist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='specialist')
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='specialist')
    phone = models.CharField(max_length=10)
    date_of_birth = models.DateField()

    def __str__(self):
        return f'{self.user.username} ({self.phone})'
 

# Disorder model  
class Disorder(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Report model 
class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='reports')
    disorder = models.ForeignKey(Disorder, on_delete=models.CASCADE, related_name='reports')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report for {self.patient.user.username} created on {self.date_created}'
    

