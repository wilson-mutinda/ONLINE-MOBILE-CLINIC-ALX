from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        "create and return a user"
        if not email:
            raise ValueError("Email is required!")
        
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(
            email = email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        
        return self.create_user(email, password, **extra_fields)

# Role model
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
# Custom user model
class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.OneToOneField(Role, on_delete=models.CASCADE, related_name='user')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return f'{self.email} ({self.role.name})'
    
# Patient Model
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return f'Patient: {self.user.first_name} {self.user.last_name}'
    
class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Specialist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='specialist_profile')
    specialization = models.OneToOneField(Specialization, on_delete=models.CASCADE, related_name='specialist')
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return f'Specialist: {self.user.username} a {self.specialization.name}'
    
class Disorder(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.SET_NULL, null=True)
    disorder = models.ForeignKey(Disorder, on_delete=models.SET_NULL, null=True, blank=True)
    diagnosis = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report for {self.patient.user.username} on {self.date_created}'
