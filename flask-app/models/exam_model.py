import psycopg2
import json

class ExamModel:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="edu_db",
            user="user",
            password="password",
            host="db"
        )

    def get_clase_aleatoria(self):
        """Obtiene una clase aleatoria con sus métodos y atributos para la actividad."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id, nombre, metodos_uml, atributos_uml, atributos, metodos
                FROM clases_exp_objetos 
                ORDER BY RANDOM() 
                LIMIT 1
            """)
            return cur.fetchone()

    def get_next_clase(self, excluded_ids):
        """Obtiene una nueva clase aleatoria excluyendo las ya utilizadas."""
        if not excluded_ids:
            return self.get_clase_aleatoria()
            
        placeholders = ','.join(['%s'] * len(excluded_ids))
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT id, nombre, metodos_uml, atributos_uml, atributos, metodos
                FROM clases_exp_objetos 
                WHERE id NOT IN ({placeholders})
                ORDER BY RANDOM() 
                LIMIT 1
            """, excluded_ids)
            return cur.fetchone()

    def guardar_resultado(self, usuario_id, clase_id, puntuacion):
        """Guarda el resultado del usuario en la base de datos."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO resultados_quiz (usuario_id, clase_id, puntuacion)
                VALUES (%s, %s, %s)
            """, (usuario_id, clase_id, puntuacion))
            self.conn.commit()