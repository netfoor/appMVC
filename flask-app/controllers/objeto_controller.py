from flask import render_template
from models.objeto_model import ObjetoModel
import json

class ObjetoController:
    def __init__(self):
        self.model = ObjetoModel()

    def explicar_objeto(self):
        """Obtiene una analogía aleatoria y la prepara para la vista."""
        analogia = self._formatear_analogia(self.model.get_random_objeto())
        return render_template('object.html', analogia=analogia)

    def _formatear_analogia(self, analogia_tuple):
        """Convierte la tupla de la base de datos en un diccionario para la vista."""
        if not analogia_tuple:
            return {}

        def parse_json(value):
            """Verifica si el valor es una cadena JSON y lo convierte, o lo devuelve tal cual."""
            if isinstance(value, str):
                return json.loads(value)
            return value

        return {
            'id': analogia_tuple[0],
            'nombre': analogia_tuple[1],
            'descripcion': analogia_tuple[2],
            'atributos': parse_json(analogia_tuple[3]),  # Verifica antes de convertir
            'metodos': parse_json(analogia_tuple[4]),    # Verifica antes de convertir
            'atributos_uml': parse_json(analogia_tuple[5]),
            'metodos_uml': parse_json(analogia_tuple[6]),
            'ejemplo_codigo': analogia_tuple[7],
            'imagen_url': analogia_tuple[8],
            'icono': analogia_tuple[9],
            'color_primario': analogia_tuple[10]
        }