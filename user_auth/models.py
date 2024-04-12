from datetime import timezone
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
# from hrmapp.models import Department, Position
from utils.reusable_methods import generate_access_token
from utils.reusable_classes import TimeStamps

    
class User(TimeStamps,AbstractUser):
    role_choices = (
            ("admin", "admin"),
            ("manager", "manager"),
            ("employee", "employee")
        )

    role = models.CharField(max_length=30, choices = role_choices, null=True, blank=True)

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(unique=True, max_length=100)
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=100)
    skills = models.TextField(blank=True, null=True)
    Education = models.CharField(max_length=50, blank=True, null=True)
    otp = models.IntegerField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    otp_generated_at = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    # emp_belongs_dept = models.ForeignKey(Department, on_delete=models.CASCADE,related_name='emp_belongs_dept1', null=True, blank=True)
    # user_position = models.ForeignKey(Position, on_delete=models.CASCADE,related_name='user_position1', null=True, blank=True)
    REQUIRED_FIELDS = ["email", "password"]

    def get_access_token(self):
        return generate_access_token(self)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Token(TimeStamps):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="token")
    
    token = models.TextField(max_length=500, unique=True, null=False, blank=False)






