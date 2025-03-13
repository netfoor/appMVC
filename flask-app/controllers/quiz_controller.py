from flask import render_template, request, session, redirect, url_for, jsonify
from models.quiz_model import QuizModel
import logging
import json

class QuizController:
    def __init__(self):
        self.model = QuizModel()
        logging.basicConfig(level=logging.DEBUG)

    def iniciar_quiz(self, tema):
        """Inicia un nuevo quiz sobre el tema seleccionado."""
        # Check if we want to start a new quiz or continue an existing one
        if 'quiz_state' not in session or request.args.get('restart') == 'true':
            # Inicializar el estado del quiz en la sesión
            session['quiz_state'] = {
                'tema': tema,
                'vidas': 3,
                'preguntas_respondidas': 0,
                'correctas': 0,
                'preguntas_vistas': []
            }
            logging.debug("Iniciando nuevo quiz para tema: %s", tema)
        
        return self.mostrar_quiz(tema)

    def mostrar_quiz(self, tema):
        """Muestra una pregunta aleatoria del tema seleccionado."""
        logging.debug(f"Mostrando quiz para el tema: {tema}")
        
        # Obtener o inicializar el estado del quiz
        if 'quiz_state' not in session:
            return self.iniciar_quiz(tema)
        
        quiz_state = session['quiz_state']
        logging.debug("Estado actual del quiz: %s", quiz_state)
        
        # Verificar si el quiz ha terminado
        if quiz_state['vidas'] <= 0 or quiz_state['preguntas_respondidas'] >= 10:
            logging.debug("Quiz terminado. Vidas: %s, Preguntas respondidas: %s", 
                        quiz_state['vidas'], quiz_state['preguntas_respondidas'])
            return self.mostrar_resultados()
        
        # Timeout handling - decrease a life if the user ran out of time
        if request.args.get('timeout') == 'true':
            quiz_state['vidas'] -= 1
            session['quiz_state'] = quiz_state
            logging.debug("Tiempo agotado. Vidas restantes: %s", quiz_state['vidas'])
            
            # Check again if the quiz should end
            if quiz_state['vidas'] <= 0:
                return self.mostrar_resultados()
        
        # Obtener una pregunta no vista antes
        pregunta = self.model.get_random_pregunta(tema, quiz_state.get('preguntas_vistas', []))
        
        if not pregunta:
            # Si no hay más preguntas disponibles
            logging.debug("No hay más preguntas disponibles")
            return self.mostrar_resultados()
            
        # Añadir la pregunta a la lista de vistas
        if 'preguntas_vistas' not in quiz_state:
            quiz_state['preguntas_vistas'] = []
        quiz_state['preguntas_vistas'].append(pregunta['id'])
        session['quiz_state'] = quiz_state
        
        # Log state for debugging
        logging.debug("Mostrando pregunta ID: %s. Estado actual: preguntas_respondidas=%s, vidas=%s", 
                    pregunta['id'], quiz_state['preguntas_respondidas'] + 1, quiz_state['vidas'])
        
        return render_template('quiz.html', 
                              pregunta=pregunta, 
                              tema=tema, 
                              vidas=quiz_state['vidas'],
                              pregunta_actual=quiz_state['preguntas_respondidas'] + 1,
                              correctas=quiz_state['correctas'])

    def verificar_respuesta(self):
        """Verifica la respuesta y devuelve el resultado como JSON."""
        pregunta_id = request.form.get('pregunta_id')
        respuesta_usuario = request.form.get('respuesta')
        logging.debug(f"Verificando respuesta para la pregunta ID: {pregunta_id}, Respuesta: {respuesta_usuario}")
        
        # Obtener la respuesta correcta
        respuesta_correcta = self.model.get_respuesta_correcta(pregunta_id)
        es_correcta = respuesta_usuario == respuesta_correcta

        # Check that we have quiz state
        if 'quiz_state' not in session:
            return jsonify({'error': 'No quiz in progress'}), 400

        # Actualizar el estado del quiz
        quiz_state = session['quiz_state']
        quiz_state['preguntas_respondidas'] += 1
        
        if es_correcta:
            quiz_state['correctas'] += 1
            logging.debug("Respuesta correcta. Correctas actuales: %s", quiz_state['correctas'])
        else:
            quiz_state['vidas'] -= 1
            logging.debug("Respuesta incorrecta. Vidas restantes: %s", quiz_state['vidas'])
            
        session.modified = True  # Explicitly mark the session as modified
        session['quiz_state'] = quiz_state
        
        # Guardar la respuesta en la base de datos si el usuario está logueado
        if 'usuario_id' in session:
            self.model.guardar_respuesta(session['usuario_id'], pregunta_id, es_correcta)
        
        # Determinar si el quiz ha terminado
        quiz_terminado = quiz_state['vidas'] <= 0 or quiz_state['preguntas_respondidas'] >= 10
        logging.debug("Quiz terminado: %s", quiz_terminado)
        
        return jsonify({
            'es_correcta': es_correcta,
            'respuesta_correcta': respuesta_correcta,
            'quiz_terminado': quiz_terminado,
            'vidas': quiz_state['vidas'],
            'correctas': quiz_state['correctas'],
            'pregunta_actual': quiz_state['preguntas_respondidas'],
            'mensaje': f"{'¡Correcto!' if es_correcta else 'Incorrecto. La respuesta correcta es: ' + respuesta_correcta}"
        })
        
    def mostrar_resultados(self):
        """Muestra los resultados finales del quiz."""
        if 'quiz_state' not in session:
            return redirect(url_for('home'))
            
        quiz_state = session['quiz_state']
        logging.debug("Mostrando resultados. Estado final: %s", quiz_state)
        
        # Use the feedback.html template for results
        return render_template('feedback.html',
                              tema=quiz_state['tema'],
                              correctas=quiz_state['correctas'],
                              total=quiz_state['preguntas_respondidas'],
                              vidas_restantes=quiz_state['vidas'])