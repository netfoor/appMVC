from dataclasses import dataclass
from typing import List, Dict

@dataclass
class InteractiveElement:
    type: str  # 'drag-drop', 'code-editor', 'quiz'
    data: Dict
    correct_answer: str

@dataclass
class ObjectLesson:
    id: int
    title: str
    description: str
    interactive_elements: List[InteractiveElement]
    examples: List[str]

class ObjectLessonManager:
    def __init__(self):
        self.lessons = self._load_lessons()
    
    def _load_lessons(self) -> Dict[int, ObjectLesson]:
        return {
            1: ObjectLesson(
                id=1,
                title="Objetos: Instancias de Clases",
                description="Un objeto es una instancia de una clase...",
                interactive_elements=[
                    InteractiveElement(
                        type="drag-drop",
                        data={
                            "question": "Arrastra los métodos a la clase Perro",
                            "options": ["ladrar", "correr", "nombre", "edad"],
                            "target": ["ladrar", "correr"]
                        },
                        correct_answer="ladrar,correr"
                    ),
                    InteractiveElement(
                        type="code-editor",
                        data={
                            "template": "mi_perro = Perro('Toby', 3)\nprint(mi_perro.nombre)",
                            "expected_output": "Toby"
                        },
                        correct_answer=""
                    )
                ],
                examples=[
                    "mi_perro = Perro('Toby', 3)",
                    "print(mi_perro.nombre)"
                ]
            )
        }
    
    def get_lesson(self, lesson_id: int) -> ObjectLesson:
        return self.lessons.get(lesson_id)