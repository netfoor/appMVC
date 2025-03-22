from flask import render_template, request, jsonify, session
from models.exam_model import ExamModel
import random
import json

class ExamController:
    def __init__(self):
        self.model = ExamModel()

    def iniciar_quiz(self):
        """Muestra la vista de la actividad UML con arrastrar y soltar."""
        # Get the current round from request parameters if available
        ronda = request.args.get('ronda', 1, type=int)
        
        # Initialize session if first round
        if ronda == 1:
            session['completed_clases'] = []
            session['puntuacion'] = 0
        
        # Update current round
        session['ronda_actual'] = ronda
        
        # Get excluded classes
        excluded_ids = session.get('completed_clases', [])
        
        # Get a class that hasn't been used yet
        clase = self.model.get_next_clase(excluded_ids) if excluded_ids else self.model.get_clase_aleatoria()
        
        if not clase:
            return "No hay clases disponibles para el quiz.", 404

        # Format methods and attributes
        metodos = json.loads(clase[2]) if isinstance(clase[2], str) else clase[2]
        atributos = json.loads(clase[3]) if isinstance(clase[3], str) else clase[3]
        
        # Mix elements for drag area
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
            vidas=session.get('vidas', 3),
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
            if not resultado:
                return jsonify({'error': 'Clase no encontrada'}), 404
                
            metodos_correctos = json.loads(resultado[0]) if isinstance(resultado[0], str) else resultado[0]
            atributos_correctos = json.loads(resultado[1]) if isinstance(resultado[1], str) else resultado[1]

        # Check if we have all required methods and attributes
        todos_metodos_presentes = all(m in metodos_usuario for m in metodos_correctos)
        todos_atributos_presentes = all(a in atributos_usuario for a in atributos_correctos)
        
        # Check if we don't have any incorrect elements
        sin_metodos_extra = all(m in metodos_correctos for m in metodos_usuario)
        sin_atributos_extra = all(a in atributos_correctos for a in atributos_usuario)
        
        es_correcto = todos_metodos_presentes and todos_atributos_presentes and sin_metodos_extra and sin_atributos_extra
        
        nuevas_vidas = vidas_actuales
        if not es_correcto:
            nuevas_vidas = max(0, vidas_actuales - 1)
        
        # Actualizar puntuación y tracking de la sesión
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
            'feedback_message': 'Correcto! Has clasificado correctamente todos los elementos.' if es_correcto else 'Incorrecto. Revisa la ubicación de los elementos.'
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

    def mostrar_resultados(self):
        """Muestra los resultados finales del examen UML."""
        # Get score and lives from URL parameters
        puntuacion = request.args.get('score', 0, type=int)
        vidas = request.args.get('vidas', 0, type=int)
        
        # Use session values as fallback if URL parameters aren't provided
        if puntuacion == 0 and 'puntuacion' in session:
            puntuacion = session.get('puntuacion', 0)
        
        if vidas == 0 and 'vidas' in session:
            vidas = session.get('vidas', 0)
        
        # Clear exam session data
        if 'completed_clases' in session:
            session.pop('completed_clases')
        if 'puntuacion' in session:
            session.pop('puntuacion')
        if 'ronda_actual' in session:
            session.pop('ronda_actual')
        if 'vidas' in session:
            session.pop('vidas')
        
        # Always provide default values for all variables used in the template
        return render_template('feedback.html',
                              puntuacion=puntuacion,
                              total_rondas=10,
                              vidas=vidas)