import json
import psycopg2
from flask import render_template
import os

class ClaseController:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="edu_db",
            user="user",
            password="password",
            host="db"
        )

    def get_analogia_aleatoria(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, nombre, descripcion, atributos, metodos, ejemplo_codigo, imagen_url, icono, color_primario
            FROM clases_analogias
            ORDER BY RANDOM()
            LIMIT 1
        """)
        analogia = cur.fetchone()
        cur.close()
        return analogia