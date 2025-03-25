from django.db import models

class UserProfile(models.Model):
    alias = models.CharField(max_length=50, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return self.alias

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
