import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import logging

class UsuarioModel:
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
            self.conn = None

    def crear_usuario(self, nombre, email, password):
        """Crea un nuevo usuario en la base de datos."""
        try:
            with self.conn.cursor() as cur:
                # Hash de la contraseña antes de almacenarla
                password_hash = generate_password_hash(password)
                
                cur.execute("""
                    INSERT INTO usuarios (nombre, email, password_hash)
                    VALUES (%s, %s, %s) RETURNING id
                """, (nombre, email, password_hash))
                
                usuario_id = cur.fetchone()[0]
                self.conn.commit()
                
                logging.debug(f"Usuario creado con ID: {usuario_id}")
                return usuario_id
        except Exception as e:
            logging.error(f"Error al crear usuario: {e}")
            self.conn.rollback()
            raise

    def obtener_por_email(self, email):
        """Obtiene un usuario por su email."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT id, nombre, email, password_hash 
                    FROM usuarios 
                    WHERE email = %s
                """, (email,))
                
                return cur.fetchone()
        except Exception as e:
            logging.error(f"Error al buscar usuario por email: {e}")
            return None

    def verificar_password(self, usuario, password):
        """Verifica si la contraseña coincide con el hash almacenado."""
        if usuario and len(usuario) >= 4:
            # Índice 3 contiene el password_hash
            return check_password_hash(usuario[3], password)
        return False

    def actualizar_ultimo_login(self, usuario_id):
        """Actualiza la fecha del último login del usuario."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    UPDATE usuarios 
                    SET ultimo_login = NOW() 
                    WHERE id = %s
                """, (usuario_id,))
                self.conn.commit()
                return True
        except Exception as e:
            logging.error(f"Error al actualizar último login: {e}")
            self.conn.rollback()
            return False