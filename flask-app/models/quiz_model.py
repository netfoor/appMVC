import psycopg2
import logging

class QuizModel:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="edu_db",
                user="user",
                password="password",
                host="db"
            )
            logging.debug("Conexión a la base de datos establecida correctamente.")
        except Exception as e:
            logging.error(f"Error al conectar a la base de datos: {e}")

    def get_random_pregunta(self, tema, preguntas_vistas=None):
        """Obtiene una pregunta aleatoria de un tema específico que no se ha visto antes."""
        try:
            if preguntas_vistas is None:
                preguntas_vistas = []
                
            with self.conn.cursor() as cur:
                query = """
                    SELECT id, enunciado, opciones FROM preguntas
                    WHERE tema = %s
                """
                
                params = [tema]
                
                # Excluir preguntas ya vistas
                if preguntas_vistas:
                    placeholders = ','.join(['%s'] * len(preguntas_vistas))
                    query += f" AND id NOT IN ({placeholders})"
                    params.extend(preguntas_vistas)
                
                query += " ORDER BY RANDOM() LIMIT 1"
                
                logging.debug(f"Ejecutando consulta SQL: {query} con parámetros: {params}")
                cur.execute(query, params)
                pregunta = cur.fetchone()
                
                if not pregunta:
                    return None
                    
                opciones = pregunta[2]
                if isinstance(opciones, list):
                    opciones = ','.join(opciones)
                
                return {
                    'id': pregunta[0],
                    'enunciado': pregunta[1],
                    'opciones': opciones.split(',')
                }
        except Exception as e:
            logging.error(f"Error al ejecutar la consulta SQL: {e}")
            return None

    def get_respuesta_correcta(self, pregunta_id):
        """Obtiene la respuesta correcta para una pregunta."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT respuesta_correcta FROM preguntas
                    WHERE id = %s
                """, (pregunta_id,))
                resultado = cur.fetchone()
                return resultado[0] if resultado else None
        except Exception as e:
            logging.error(f"Error al obtener la respuesta correcta: {e}")
            return None

    def guardar_respuesta(self, usuario_id, pregunta_id, es_correcta):
        """Guarda la respuesta del usuario."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO respuestas (usuario_id, pregunta_id, es_correcta)
                    VALUES (%s, %s, %s)
                """, (usuario_id, pregunta_id, es_correcta))
                self.conn.commit()
        except Exception as e:
            logging.error(f"Error al guardar la respuesta: {e}")