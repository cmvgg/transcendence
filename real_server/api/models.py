from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

"""
class Userstatistics(models.Model):
    alias = models.CharField(max_length=50, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.alias

    def win_rate(self):
        total = self.wins + self.losses
        return self.wins / total if total > 0 else 0

    def total_games(self):
        return self.wins + self.losses

    class Meta:
        ordering = ['-wins', 'alias']
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
"""

class TournamentStats(models.Model):
    username = models.CharField(max_length=100, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    tournaments_won = models.IntegerField(default=0)

    def __str__(self):
        #return f"{self.username} - {self.wins}W/{self.losses}L"
        return self.username
    
    def win_rate(self):
        """Calcula el porcentaje de victorias"""
        total_games = self.wins + self.losses
        if total_games == 0:
            return 0.0
        return self.wins / total_games
    
    def total_games(self):
        """Retorna el total de partidas jugadas"""
        return self.wins + self.losses

    class Meta:
        verbose_name = "Tournament Stats"
        verbose_name_plural = "Tournament Stats"
        ordering = ['-wins', 'username']

class UserProfile(models.Model):
    #user_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE , primary_key=True)  # Descomenta si quieres usar relación
    username = models.CharField(max_length=50, unique=True)
    alias = models.CharField(max_length=50, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='media/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.alias  # Cambiado para que funcione correctamente
    
    def win_rate(self):
        """Calcula el porcentaje de victorias"""
        total_games = self.wins + self.losses
        if total_games == 0:
            return 0.0
        return self.wins / total_games
    
    def total_games(self):
        """Retorna el total de partidas jugadas"""
        return self.wins + self.losses
    
    class Meta:
        ordering = ['-wins', 'alias']  # Ordenar por victorias descendente, luego por alias
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'

class Tournament(models.Model):
    # Campo para el ID del torneo
    # tournament_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField('UserProfile', related_name='tournaments')   
    status = models.CharField(
        max_length=20,
        choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('finished', 'Finished')],
        default='upcoming'
    )
    end_date = models.DateTimeField(null=True, blank=True)
    winner = models.ForeignKey('UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='won_tournaments')
    is_active = models.BooleanField(default=True)  # Mantengo compatibilidad con el código existente

    """ def save(self, *args, **kwargs):
        # Asignar un ID personalizado si no existe
        if not self.custom_id:
            last_tournament = Tournament.objects.order_by('-custom_id').first()
            self.custom_id = (last_tournament.custom_id + 1) if last_tournament else 1
        super().save(*args, **kwargs) """

    def __str__(self):
        return self.name

    def clean(self):
        # Se requiere al menos 4 participantes (ajusta este número según tus necesidades)
        if self.participants.count() < 4:
            raise ValidationError('A tournament must have at least 4 participants.')

    class Meta:
        ordering = ['-start_date']

""" #Nueva clase para almacenar estadísticas de torneos por usuario
# Esta clase almacena estadísticas de torneos por usuario, como victorias, derrotas y
# torneos ganados. Se relaciona con el modelo UserProfile para obtener el alias del usuario.
class UserTournamentStats(models.Model):
    user_id = models.PositiveIntegerField()
    username = models.CharField(max_length=100)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    tournaments_won = models.IntegerField(default=0)

    class Meta:
        verbose_name = "User Tournament Stats"
        verbose_name_plural = "User Tournament Stats" """

class ProfileData(models.Model):
    # modelo para endpoint get que consulte los datos del jugador
    alias = models.CharField(max_length=50)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)  # Agregué losses para consistencia
    avatar = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return f"{self.alias} - {self.wins}W"
    
    def win_rate(self):
        """Calcula el porcentaje de victorias"""
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