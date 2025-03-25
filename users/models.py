from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ("user", "User"),
        ("club_member", "Club Member"),
        ("club_leader", "Club Leader"),
        ("activity_center_admin", "Activity Center Admin"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", default="profile_pictures/default.jpg")
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    has_voted = models.BooleanField(default=False)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="user")

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name} ({self.email})"

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_admin or self.is_superuser

    def get_role(self):
        return self.role.lower()


class Membership(models.Model):
    MEMBERSHIP_TYPE_CHOICES = [
        ("pending", "Pending"),
        ("member", "Member"),
        ("leader", "Leader"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    club = models.ForeignKey('clubs.Club', on_delete=models.CASCADE, related_name="memberships", null=True)
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_TYPE_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "club")

    def __str__(self):
        return f"{self.user.name} - {self.club.name} ({self.membership_type})"
