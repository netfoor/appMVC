import psycopg2

class SelectModel:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="edu_db",
                user="user",
                password="password",
                host="db"
            )
        except Exception as e:
            print(f"Error al conectar a la base de datos: {str(e)}")
            raise

    def get_all_clases(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, nombre FROM clases_exp_objetos ORDER BY nombre")
                return cur.fetchall()
        except Exception as e:
            print(f"Error al obtener todas las clases: {str(e)}")
            return []

    def get_clase_by_id(self, clase_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM clases_exp_objetos WHERE id = %s", (clase_id,))
                return cur.fetchone()
        except Exception as e:
            print(f"Error al obtener la clase por ID: {str(e)}")
            return None