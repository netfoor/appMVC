from flask import request, render_template
from services.ai_service import AIService

class AIController:
    def __init__(self):
        self.ai_service = AIService()

    def explain_concept(self):
        text = request.form.get('concept')
        explanation = self.ai_service.explain(text)
        return render_template('explain/explanation.html', concept=text, explanation=explanation)