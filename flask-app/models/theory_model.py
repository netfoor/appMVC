from dataclasses import dataclass
from typing import List, Dict

@dataclass
class InteractiveElement:
    type: str  # 'drag-drop', 'code-editor', 'quiz'
    data: Dict
    correct_answer: str

@dataclass
class TheoryLesson:
    id: int
    title: str
    description: str
    interactive_elements: List[InteractiveElement]
    examples: List[str]

class LessonManager:
    def __init__(self):
        self.lessons = self._load_lessons()
    
    def _load_lessons(self) -> Dict[int, TheoryLesson]:
        return {
            1: TheoryLesson(
                id=1,
                title="Clases: Planos de Construcción",
                description="Una clase es como un molde para crear objetos...",
                interactive_elements=[
                    InteractiveElement(
                        type="drag-drop",
                        data={
                            "question": "Arrastra los atributos a la clase Perro",
                            "options": ["nombre", "edad", "ladrar", "raza"],
                            "target": ["nombre", "edad", "raza"]
                        },
                        correct_answer="nombre,edad,raza"
                    ),
                    InteractiveElement(
                        type="code-editor",
                        data={
                            "template": "class Perro:\n    def __init__(self, nombre, edad):\n        self.nombre = nombre\n        self.edad = edad",
                            "expected_output": "Perro(nombre='Toby', edad=3)"
                        },
                        correct_answer=""
                    )
                ],
                examples=[
                    "class Perro:\n    def __init__(self, nombre):\n        self.nombre = nombre",
                    "mi_perro = Perro('Toby')"
                ]
            )
        }
    
    def get_lesson(self, lesson_id: int) -> TheoryLesson:
        return self.lessons.get(lesson_id)