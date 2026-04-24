from django.contrib.auth.models import User
from django.db import models


# Create your models here.
ROLE_CHOICES = [
    ("fiction_employee", "Fiction Employee"),
    ("nonfiction_employee", "Non-Fiction Employee"),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=True, null=True)
    def __str__(self):
        return self.user.username