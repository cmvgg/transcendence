from django.db import models
from django.core.exceptions import ValidationError

class UserProfile(models.Model):
    alias = models.CharField(max_length=50, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return self.alias

    def win_rate(self):
        total = self.wins + self.losses
        return self.wins / total if total > 0 else 0

    class Meta:
        ordering = ['-wins', 'alias']

class Tournament(models.Model):
    #Campo para el ID del torneo
    #tournament_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField('UserProfile', related_name='tournaments')
    
    status = models.CharField(
        max_length=20,
        choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('finished', 'Finished')],
        default='upcoming'
    )
    
    end_date = models.DateTimeField(null=True, blank=True)

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
