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
            # Asegúrate de que la consulta apunte a la nueva tabla
            cur.execute("SELECT * FROM clases_exp_objetos ORDER BY RANDOM() LIMIT 1")
            return cur.fetchone()