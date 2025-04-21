from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alias = models.CharField(max_length=50, unique=True)
    
    # Add any additional fields you need for user profiles
    
    def __str__(self):
        return self.user.username