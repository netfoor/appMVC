from flask import render_template
from models.select_model import SelectModel
from flask import render_template, request
import json

class SelectController:
    def __init__(self):
        self.model = SelectModel()

    def seleccionar_objeto(self):
        """Muestra la vista de selección y maneja la elección del usuario"""
        clases = self.model.get_all_clases()
        
        clase_id = request.args.get('clase_id')
        analogia = None
        
        if clase_id:
            clase_data = self.model.get_clase_by_id(clase_id)
            if clase_data:
                analogia = self._formatear_analogia(clase_data)
        
        return render_template('seleccion_objeto.html', 
                             clases=clases,
                             analogia=analogia,
                             clase_seleccionada=clase_id)

    def _formatear_analogia(self, analogia_tuple):
        """Convierte la tupla de la base de datos en un diccionario para la vista."""
        if not analogia_tuple:
            return {}

        return {
            'id': analogia_tuple[0],
            'nombre': analogia_tuple[1],
            'descripcion': analogia_tuple[2],
            'atributos': [attr.replace(':', '=') for attr in (json.loads(analogia_tuple[3]) if isinstance(analogia_tuple[3], str) else analogia_tuple[3])],
            'metodos': [method + '()' for method in (json.loads(analogia_tuple[4]) if isinstance(analogia_tuple[4], str) else analogia_tuple[4])],
            'ejemplo_codigo': analogia_tuple[5],
            'imagen_url': analogia_tuple[6],
            'icono': analogia_tuple[7],
            'color_primario': analogia_tuple[8]
        }