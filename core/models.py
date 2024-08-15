from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100,unique=True)  # Required field
    phone_number = models.CharField(max_length=15,unique=True)  # Required field
    review = models.TextField()  # Required field
    email = models.EmailField(blank=True, null=True)  # Optional field

    roles = models.ManyToManyField(Role, related_name='users', blank=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ('view_dashboard', 'Can view dashboard'),
            ('add_dashboard', 'Can add dashboard'),
            ('delete_dashboard', 'Can delete dashboard'),
            ('change_dashboard', 'Can change dashboard'),
            ('view_menu', 'Can view menu'),
            ('add_menu', 'Can add menu'),
            ('delete_menu', 'Can delete menu'),
            ('change_menu', 'Can change menu'),
        ]


class Review(models.Model):
    DEPARTMENT_CHOICES = [
        ('BOD', 'Board of Directors'),
        ('Manager', 'Manager'),
        ('Help Desk', 'Help Desk'),
        ('Gov Official', 'Government Official'),
    ]

    PURPOSE_CHOICES = [
        ('Business', 'Business Meeting'),
        ('Support', 'Customer Support'),
        ('Consultation', 'Consultation'),
        ('Other', 'Other'),
    ]

    CUSTOM_FIELD = [
        ('Business', 'Business Meeting'),
        ('Support', 'Customer Support'),
        ('Consultation', 'Consultation'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)  # Required
    email = models.EmailField(blank=True, null=True)  # Optional
    phone_number = models.IntegerField(max_length=10)  # Required and unique
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='Help Desk')  # Department field
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='Other')  # Purpose field
    other_purpose = models.CharField(max_length=255, blank=True, null=True)  # Optional additional detail
    review = models.TextField(blank=True)  # Visitor's review
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for review creation

    def __str__(self):
        return f"Review by {self.name or 'Anonymous'}"