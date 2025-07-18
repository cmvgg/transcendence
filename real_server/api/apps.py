from django.apps import AppConfig
from django.db import connection
from django.db.models.signals import post_migrate


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Conectar la señal post_migrate
        post_migrate.connect(create_user_tournament_stats_table, sender=self)


def create_user_tournament_stats_table(sender, **kwargs):
    """
    Crea la tabla api_userTournamentStats automáticamente después de las migraciones y copia los datos existentes.
    """
    try:
        with connection.cursor() as cursor:
            # Crear la tabla
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_userTournamentStats (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    username VARCHAR(100) NOT NULL,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    tournaments_won INTEGER DEFAULT 0
                );
            """)

            # Copiar los datos
            cursor.execute("""
                INSERT INTO api_userTournamentStats (user_id, username, wins, losses, tournaments_won)
                SELECT 
                    u.id AS user_id,
                    u.alias AS username,
                    u.wins AS wins,
                    u.losses AS losses,
                    COUNT(CASE WHEN t.id IS NOT NULL AND t.status = 'finished' THEN 1 ELSE NULL END) AS tournaments_won
                FROM api_userprofile u
                LEFT JOIN api_tournament_participants tp ON tp.userprofile_id = u.id
                LEFT JOIN api_tournament t ON t.id = tp.tournament_id
                GROUP BY u.id, u.alias, u.wins, u.losses
            """)
            print("Tabla api_userTournamentStats creada y datos copiados correctamente.")
    except Exception as e:
        print(f"Error al crear o llenar la tabla api_userTournamentStats: {e}")

