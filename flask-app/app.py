from flask import Flask, render_template, request # Import request, 
from controllers.theory_controller import TheoryController
from controllers.clase_controller import ClaseController
from controllers.objeto_controller import ObjetoController
import json
from controllers.auth_controller import AuthController
from controllers.select_controller import SelectController
from controllers.quiz_controller import QuizController
from controllers.exam_controller import ExamController
from dotenv import load_dotenv
import os

app = Flask(__name__, static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Recarga automática de templates

load_dotenv()  # Load environment variables from .env file

app.secret_key = 'fortino'  # Clave secreta para las sesiones

theory_controller = TheoryController()
clase_controller = ClaseController()
objeto_controller = ObjetoController()
select_controller = SelectController()
auth_controller = AuthController()
quiz_controller = QuizController()
exam_controller = ExamController()

#@app.route('/theory/<int:lesson_id>')
#def theory_lesson(lesson_id):
#    lesson = theory_controller.get_lesson_data(lesson_id)
#    return render_template('theory/lesson_1.html', lesson=lesson)
@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return auth_controller.registro()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return auth_controller.login()

@app.route('/logout')
def logout():
    return auth_controller.logout()

@app.route('/exam')
def exam():
    return exam_controller.iniciar_quiz()

app.add_url_rule('/seleccion', 
                 view_func=select_controller.seleccionar_objeto, 
                 methods=['GET'])

# Ruta del Quiz
@app.route('/quiz/<tema>')
def iniciar_quiz(tema):
    return quiz_controller.iniciar_quiz(tema)

@app.route('/verificar-respuesta', methods=['POST'])
def verificar_respuesta():
    return quiz_controller.verificar_respuesta()

@app.route('/verificar-examen', methods=['POST'])
def verificar_examen():
    return exam_controller.verificar_respuesta()

@app.route('/resultados-quiz')
def mostrar_resultados():
    # Check if we're coming from exam or quiz
    from_exam = request.args.get('exam') == 'true'
    
    if from_exam:
        return exam_controller.mostrar_resultados()
    else:
        # Make sure quiz_controller handles undefined variables
        return quiz_controller.mostrar_resultados()

@app.route('/clase')
def mostrar_clase():
    return clase_controller.explicar_clase()

@app.route('/objeto')
def objeto():
    return ObjetoController().explicar_objeto()

if __name__ == '__main__':
    app.run(host='0.0.0.0')