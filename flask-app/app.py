from flask import Flask, render_template
from controllers.theory_controller import TheoryController
from controllers.clase_controller import ClaseController
import json

app = Flask(__name__, static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Recarga automática de templates

theory_controller = TheoryController()
clase_controller = ClaseController()

@app.route('/theory/<int:lesson_id>')
def theory_lesson(lesson_id):
    lesson = theory_controller.get_lesson_data(lesson_id)
    return render_template('theory/lesson_1.html', lesson=lesson)

@app.route('/clase')
def mostrar_clase():
    analogia = clase_controller.get_analogia_aleatoria()
    
    # Convertir los atributos y métodos de JSON a listas
    analogia = list(analogia)  # Convertir tupla a lista
    try:
        analogia[3] = json.loads(analogia[3])  # Convertir atributos de JSON a lista
        analogia[4] = json.loads(analogia[4])  # Convertir métodos de JSON a lista
    except (TypeError, json.JSONDecodeError) as e:
        # Manejar el caso en que los datos no sean JSON válido
        print(f"Error decodificando JSON: {e}")
        analogia[3] = analogia[3].split(',') if isinstance(analogia[3], str) else []
        analogia[4] = analogia[4].split(',') if isinstance(analogia[4], str) else []
    
    # Pasar la analogía a la plantilla
    return render_template('theory/clase.html', analogia={
        "id": analogia[0],
        "nombre": analogia[1],
        "descripcion": analogia[2],
        "atributos": analogia[3],
        "metodos": analogia[4],
        "ejemplo_codigo": analogia[5],
        "imagen_url": analogia[6],
        "icono": analogia[7],
        "color_primario": analogia[8]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0')