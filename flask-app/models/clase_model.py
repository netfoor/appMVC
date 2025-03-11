import psycopg2
import random

class ClaseModel:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="edu_db",
            user="user",
            password="password",
            host="db"
        )

    def get_random_analogia(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM clases_analogias ORDER BY RANDOM() LIMIT 1")
        analogia = cur.fetchone()
        cur.close()
        return analogia