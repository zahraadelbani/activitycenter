from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_admin or self.is_superuser

class ClubLeader(User):
    club_name = models.CharField(max_length=255)  # Example additional field
    club_description = models.TextField()

    def __str__(self):
        return f"Club Leader: {self.name} ({self.club_name})"

class Executive(User):
    department = models.CharField(max_length=255)  # Example additional field

    def __str__(self):
        return f"Executive: {self.name} ({self.department})"

class Rector(User):
    university_name = models.CharField(max_length=255)  # Example additional field

    def __str__(self):
        return f"Rector: {self.name} ({self.university_name})"

class ActivityCenterAdmin(User):
    center_location = models.CharField(max_length=255)  # Example additional field

    def __str__(self):
        return f"Activity Center Admin: {self.name} ({self.center_location})"

class ClubMember(User):
    club = models.ForeignKey(ClubLeader, on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return f"Club Member: {self.name} (Club: {self.club.club_name})"

