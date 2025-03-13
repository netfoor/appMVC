import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioModel:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="edu_db",
            user="user",
            password="password",
            host="db"
        )

    def crear_usuario(self, nombre, email, password):
        """Crea un nuevo usuario con contraseña hasheada."""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)",
                (nombre, email, generate_password_hash(password))
            )
            self.conn.commit()

    def obtener_por_email(self, email):
        """Obtiene un usuario por su email."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            return cur.fetchone()

    def verificar_password(self, usuario, password):
        """Verifica si la contraseña coincide con el hash almacenado."""
        return check_password_hash(usuario[3], password)