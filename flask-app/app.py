from flask import Flask, render_template
from controllers.theory_controller import TheoryController

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Recarga automática de templates

theory_controller = TheoryController()

@app.route('/theory/<int:lesson_id>')
def theory_lesson(lesson_id):
    lesson = theory_controller.get_lesson_data(lesson_id)
    return render_template('theory/lesson_1.html', lesson=lesson)

if __name__ == '__main__':
    app.run(host='0.0.0.0')