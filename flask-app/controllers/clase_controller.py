from flask import render_template
from models.clase_model import ClaseModel

class ClaseController:
    def __init__(self):
        self.model = ClaseModel()

    def explicar_clase(self):
        """Obtiene una analogía aleatoria y la prepara para la vista."""
        analogia = self._formatear_analogia(self.model.get_random_analogia())
        return render_template('clase.html', analogia=analogia)

    def _formatear_analogia(self, analogia_tuple):
        """Convierte la tupla de la base de datos en un diccionario para la vista."""
        if not analogia_tuple:
            return {}

        return {
            'id': analogia_tuple[0],
            'nombre': analogia_tuple[1],
            'descripcion': analogia_tuple[2],
            'atributos': analogia_tuple[3],
            'metodos': analogia_tuple[4],
            'ejemplo_codigo': analogia_tuple[5],
            'imagen_url': analogia_tuple[6],
            'icono': analogia_tuple[7],
            'color_primario': analogia_tuple[8]
        }