from django.apps import AppConfig
from django.db import connection


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        """
        Crea la tabla api_userTournamentStats automáticamente al iniciar el proyecto y copia los datos existentes.
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
                    )
                """)

                # Copiar los datos
                cursor.execute("""
                    INSERT INTO api_userTournamentStats (user_id, username, wins, losses, tournaments_won)
                    SELECT 
                        u.id AS user_id,
                        u.alias AS username,
                        u.wins AS wins,
                        u.losses AS losses,
                        COUNT(CASE WHEN t.id IS NOT NULL AND u.losses = 0 THEN 1 ELSE NULL END) AS tournaments_won
                    FROM api_userprofile u
                    LEFT JOIN api_tournament_participants tp ON tp.userprofile_id = u.id
                    LEFT JOIN api_tournament t ON t.id = tp.tournament_id AND t.status = 'finished'
                    GROUP BY u.id, u.alias, u.wins, u.losses
                """)
        except Exception as e:
            print(f"Error al crear o llenar la tabla api_userTournamentStats: {e}")
            
