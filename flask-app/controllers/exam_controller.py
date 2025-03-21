from flask import render_template, request, jsonify, session
from models.exam_model import ExamModel
import random
import json

class ExamController:
    def __init__(self):
        self.model = ExamModel()

    def iniciar_quiz(self):
        """Muestra la vista de la actividad UML con arrastrar y soltar."""
        # Inicializar o reiniciar el seguimiento de la sesión
        session['completed_clases'] = []
        session['puntuacion'] = 0
        session['ronda_actual'] = 1
        
        clase = self.model.get_clase_aleatoria()
        if not clase:
            return "No hay clases disponibles para el quiz.", 404

        # Formatear los métodos y atributos para la actividad
        metodos = json.loads(clase[2]) if isinstance(clase[2], str) else clase[2]
        atributos = json.loads(clase[3]) if isinstance(clase[3], str) else clase[3]
        
        # Mezclar todos los elementos juntos para el área de arrastre
        elementos = []
        for metodo in metodos:
            elementos.append({"tipo": "metodo", "valor": metodo})
        for atributo in atributos:
            elementos.append({"tipo": "atributo", "valor": atributo})
        
        elementos_mezclados = random.sample(elementos, len(elementos))

        return render_template(
            'exam.html',
            clase=clase,
            elementos=elementos_mezclados,
            vidas=3,
            ronda=session['ronda_actual'],
            total_rondas=10
        )

    def verificar_respuesta(self):
        data = request.get_json()
        clase_id = data.get('clase_id')
        metodos_usuario = data.get('metodos', [])
        atributos_usuario = data.get('atributos', [])
        vidas_actuales = data.get('vidas', 3)
        
        # Obtener los datos correctos
        with self.model.conn.cursor() as cur:
            cur.execute("SELECT metodos_uml, atributos_uml FROM clases_exp_objetos WHERE id = %s", (clase_id,))
            resultado = cur.fetchone()
            metodos_correctos = json.loads(resultado[0]) if isinstance(resultado[0], str) else resultado[0]
            atributos_correctos = json.loads(resultado[1]) if isinstance(resultado[1], str) else resultado[1]

        # Calcular errores
        errores_metodos = sum(1 for metodo in metodos_usuario if metodo not in metodos_correctos)
        errores_atributos = sum(1 for atributo in atributos_usuario if atributo not in atributos_correctos)
        
        elementos_faltantes = len(metodos_correctos) - len(metodos_usuario) + len(atributos_correctos) - len(atributos_usuario)
        total_errores = errores_metodos + errores_atributos + max(0, elementos_faltantes)
        
        nuevas_vidas = vidas_actuales - (1 if total_errores > 0 else 0)
        nuevas_vidas = max(0, nuevas_vidas)
        
        # Actualizar puntuación y tracking de la sesión
        es_correcto = total_errores == 0
        if es_correcto:
            session['puntuacion'] = session.get('puntuacion', 0) + 1
            session['completed_clases'] = session.get('completed_clases', []) + [clase_id]
            session['ronda_actual'] = session.get('ronda_actual', 1) + 1
        
        # Verificar si el juego ha terminado
        juego_terminado = (nuevas_vidas == 0) or (session.get('ronda_actual', 1) > 10)
        siguiente_clase = None
        
        if es_correcto and not juego_terminado:
            siguiente_clase = self.model.get_next_clase(session.get('completed_clases', []))
            if not siguiente_clase:
                juego_terminado = True

        return jsonify({
            'es_correcto': es_correcto,
            'vidas': nuevas_vidas,
            'puntuacion': session.get('puntuacion', 0),
            'ronda_actual': session.get('ronda_actual', 1),
            'juego_terminado': juego_terminado,
            'siguiente_clase': siguiente_clase[1] if siguiente_clase else None,
            'siguiente_clase_id': siguiente_clase[0] if siguiente_clase else None,
            'siguiente_elementos': self._formatear_elementos(siguiente_clase) if siguiente_clase else None
        })
        
    def _formatear_elementos(self, clase):
        """Formatea los elementos de una clase para la interfaz."""
        metodos = json.loads(clase[2]) if isinstance(clase[2], str) else clase[2]
        atributos = json.loads(clase[3]) if isinstance(clase[3], str) else clase[3]
        
        elementos = []
        for metodo in metodos:
            elementos.append({"tipo": "metodo", "valor": metodo})
        for atributo in atributos:
            elementos.append({"tipo": "atributo", "valor": atributo})
        
        return random.sample(elementos, len(elementos))