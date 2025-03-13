import psycopg2

class ClaseModel:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="edu_db",
            user="user",
            password="password",
            host="db"
        )

    def get_random_analogia(self):
        """Obtiene una analogía aleatoria de la base de datos."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM clases_analogias ORDER BY RANDOM() LIMIT 1")
                return cur.fetchone()
        except Exception as e:
            print(f"Error al obtener la analogía: {e}")
            return None