from models.objeto_model import ObjectLessonManager, ObjectLesson
from services.interactivity_service import InteractivityService

class ObjetoController:
    def __init__(self):
        self.lesson_manager = ObjectLessonManager()
        self.interactivity_service = InteractivityService()
    
    def get_lesson_data(self, lesson_id: int) -> ObjectLesson:
        return self.lesson_manager.get_lesson(lesson_id)
    
    def check_drag_drop_answer(self, lesson_id: int, user_answer: list) -> bool:
        lesson = self.get_lesson_data(lesson_id)
        for element in lesson.interactive_elements:
            if element.type == "drag-drop":
                return ",".join(user_answer) == element.correct_answer
        return False
    
    def validate_code_exercise(self, lesson_id: int, user_code: str) -> dict:
        lesson = self.get_lesson_data(lesson_id)
        return self.interactivity_service.validate_python_code(user_code, lesson.interactive_elements[1].data["expected_output"])