from flask import Flask, render_template, request # Import request
from controllers.theory_controller import TheoryController
from controllers.clase_controller import ClaseController
from controllers.objeto_controller import ObjetoController
import json

app = Flask(__name__, static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Recarga automática de templates

theory_controller = TheoryController()
clase_controller = ClaseController()
objeto_controller = ObjetoController()


#@app.route('/theory/<int:lesson_id>')
#def theory_lesson(lesson_id):
#    lesson = theory_controller.get_lesson_data(lesson_id)
#    return render_template('theory/lesson_1.html', lesson=lesson)

@app.route('/clase')
def mostrar_clase():
    return clase_controller.explicar_clase()

@app.route('/objeto')
def objeto():
    return ObjetoController().explicar_objeto()

if __name__ == '__main__':
    app.run(host='0.0.0.0')