# objeto_model.py
import psycopg2

class ObjetoModel:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="edu_db",
            user="user",
            password="password",
            host="db"
        )

    def get_random_objeto(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM objetos_analogias ORDER BY RANDOM() LIMIT 1")
            return cur.fetchone()