from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from clubs.models import Club

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
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
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
    
    def get_role(self):
        """Determine the role of the user based on the subclass"""
        if hasattr(self, 'clubleader'):
            return "Club Leader"
        elif hasattr(self, 'executive'):
            return "Executive"
        elif hasattr(self, 'rector'):
            return "Rector"
        elif hasattr(self, 'activitycenteradmin'):
            return "Activity Center Admin"
        elif hasattr(self, 'clubmember'):
            return "Club Member"
        elif self.is_superuser:
            return "Superuser"
        elif self.is_staff:
            return "Staff"
        else:
            return "User"

class ClubLeader(User):
    club = models.OneToOneField(
        "clubs.Club",  # ✅ Reference to Club
        on_delete=models.SET_NULL,
        null=True,  # ✅ Allow null values
        blank=True,  # ✅ Allow blank forms
        related_name="club_leader"
    )
    club_description = models.TextField()

    def __str__(self):
        club_name = self.club.name if self.club else "No Club Assigned"
        return f"Club Leader: {self.name} ({club_name})"

class Executive(User):
    department = models.CharField(max_length=255)

    def __str__(self):
        return f"Executive: {self.name} ({self.department})"

class Rector(User):
    university_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Rector: {self.name} ({self.university_name})"

class ActivityCenterAdmin(User):
    center_location = models.CharField(max_length=255)

    def __str__(self):
        return f"Activity Center Admin: {self.name} ({self.center_location})"

class ClubMember(models.Model):  # ✅ Don't inherit from User directly
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_club_memberships"  # ✅ UNIQUE related_name
    )

    club = models.ForeignKey(
        "clubs.Club",
        on_delete=models.CASCADE,
        related_name="memberships"  # ✅ UNIQUE related_name
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Club Member: {self.user.name} (Club: {self.club.name})"