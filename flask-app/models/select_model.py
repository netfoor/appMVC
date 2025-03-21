import psycopg2

class SelectModel:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="edu_db",
            user="user",
            password="password",
            host="db"
        )

    def get_all_clases(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, nombre FROM clases_exp_objetos ORDER BY nombre")
            return cur.fetchall()

    def get_clase_by_id(self, clase_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM clases_exp_objetos WHERE id = %s", (clase_id,))
            return cur.fetchone()