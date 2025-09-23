from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField
from django.contrib.auth.signals import user_logged_in, user_logged_out

class MatchHistory(models.Model):
    winner = models.CharField(max_length=100)
    loser = models.CharField(max_length=100)
    w_points = models.IntegerField(default=0)
    l_points = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    type_game = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.winner} defeated {self.loser} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}"


class UsersInTournament(models.Model):
    username = models.CharField(max_length=100, unique=True)
    avatar = ResizedImageField(size=[200,200], upload_to='', blank=True, null=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    tournaments_won = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} - {self.wins}W/{self.losses}L"

    class Meta:
        verbose_name = "Users In Tournament"
        verbose_name_plural = "Users In Tournament"
        ordering = ['-wins', 'username']
        
#USER
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = ResizedImageField(size=[200,200], upload_to='', blank=True, null=True)
    friends = ArrayField(
        models.IntegerField(),
        size=100,
        blank=True,
        default=list,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wins = models.IntegerField(default=0, null = True)
    losses = models.IntegerField(default=0, blank=True, null=True)
    tournaments_won = models.IntegerField(default=0, blank=True, null=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        new_user = instance
        new_user.avatar = instance.profile.avatar
        new_user.save()

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):    
    user.profile.is_online = True
    user.profile.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.profile.is_online = False
    user.profile.save()


 #USER END       

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('finished', 'Finished')],
        default='upcoming'
    )
    
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.participants.count() < 4:
            raise ValidationError('A tournament must have at least 4 participants.')

    class Meta:
        ordering = ['-start_date']

class ProfileData(models.Model):
    alias = models.CharField(max_length=50)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.alias} - {self.wins}W"
    
    def win_rate(self):
        total_games = self.wins + self.losses
        if total_games == 0:
            return 0.0
        return self.wins / total_games

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    player1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='matches_as_player1')
    player2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='matches_as_player2')
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.player1.alias} vs {self.player2.alias}"
    
    def winner(self):
        """Retorna el ganador del match"""
        if not self.is_finished:
            return None
        return self.player1 if self.player1_score > self.player2_score else self.player2
    
    def loser(self):
        """Retorna el perdedor del match"""
        if not self.is_finished:
            return None
        return self.player2 if self.player1_score > self.player2_score else self.player1
    
    class Meta:
        ordering = ['-date_played']
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

