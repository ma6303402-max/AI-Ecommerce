from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('administrator', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    preferred_categories = models.JSONField(default=list, blank=True)
    
    def is_administrator(self):
        return self.role == 'administrator' or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
