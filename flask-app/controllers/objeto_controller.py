from flask import render_template
from models.objeto_model import ObjetoModel

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