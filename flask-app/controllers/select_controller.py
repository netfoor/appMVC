from flask import render_template, request
from models.select_model import SelectModel
import json

class SelectController:
    def __init__(self):
        self.model = SelectModel()

    def seleccionar_objeto(self):
        """Muestra la vista de selección y maneja la elección del usuario"""
        try:
            # Obtener todas las clases disponibles
            clases = self.model.get_all_clases()
            
            # Obtener la clase seleccionada (si existe)
            clase_id = request.args.get('clase_id')
            analogia = None
            
            if clase_id:
                # Obtener los datos de la clase seleccionada
                clase_data = self.model.get_clase_by_id(clase_id)
                if clase_data:
                    analogia = self._formatear_analogia(clase_data)
            
            # Renderizar la plantilla con los datos
            return render_template('seleccion_objeto.html', 
                                 clases=clases,
                                 analogia=analogia,
                                 clase_seleccionada=clase_id)
        except Exception as e:
            # Manejar errores y mostrar un mensaje en el servidor
            print(f"Error en seleccionar_objeto: {str(e)}")
            return "Error al cargar la página. Por favor, revisa los logs del servidor.", 500

    def _formatear_analogia(self, analogia_tuple):
        """Convierte la tupla de la base de datos en un diccionario para la vista."""
        if not analogia_tuple:
            return {}

        try:
            # Convertir JSON a listas si es necesario
            atributos = json.loads(analogia_tuple[3]) if isinstance(analogia_tuple[3], str) else analogia_tuple[3]
            metodos = json.loads(analogia_tuple[4]) if isinstance(analogia_tuple[4], str) else analogia_tuple[4]
            atributos_uml = json.loads(analogia_tuple[5]) if isinstance(analogia_tuple[5], str) else analogia_tuple[5]
            metodos_uml = json.loads(analogia_tuple[6]) if isinstance(analogia_tuple[6], str) else analogia_tuple[6]
            
            return {
                'id': analogia_tuple[0],
                'nombre': analogia_tuple[1],
                'descripcion': analogia_tuple[2],
                'atributos': [attr.replace(':', '=') for attr in atributos],
                'metodos': [method + '()' for method in metodos],
                'atributos_uml': atributos_uml,
                'metodos_uml': metodos_uml,
                'ejemplo_codigo': analogia_tuple[7],
                'imagen_url': analogia_tuple[8],
                'icono': analogia_tuple[9],
                'color_primario': analogia_tuple[10]
            }
        except Exception as e:
            # Manejar errores en el formato de los datos
            print(f"Error al formatear analogía: {str(e)}")
            return {}