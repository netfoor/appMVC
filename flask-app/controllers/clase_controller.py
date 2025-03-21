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
        
        # Formatear métodos y atributos para UML
        atributos = [f"+ {a}" if not a.startswith(('-', '+', '#')) else a 
                     for a in analogia_tuple[3]]
        metodos = [f"{m}()" if '(' not in m else m 
                   for m in analogia_tuple[4]]

        return {
            'id': analogia_tuple[0],
            'nombre': analogia_tuple[1],
            'descripcion': analogia_tuple[2],
            'atributos': analogia_tuple[3],
            'metodos': analogia_tuple[4],
            'ejemplo_codigo': analogia_tuple[5],
            'imagen_url': analogia_tuple[6],
            'icono': analogia_tuple[7],
            'color_primario': analogia_tuple[8],
            'atributos_uml': atributos,  
            'metodos_uml': metodos,     
            'cita_apa': ""
            """Los objetos se crean a partir de clases, y las clases sirven como plantillas para crear objetos. Utilicemos una analogía. Piensa en la palabra persona. Cuando hablamos de una persona no nos referimos a ninguna persona en particular, solo a la idea de la persona. Una persona tiene un nombre, una edad, una estatura, etc. Esa es la clase, la plantilla." (Make It Real, s.f.).\n"""
            "Make It Real. (s.f.). Clases y objetos. En Programación orientada por objetos en Ruby. Recuperado de https://makeitrealcamp.gitbook.io/programacion-orientada-por-objetos-en-ruby/clases-y-objetos"
        }

