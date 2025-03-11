# services/ai_service.py
import requests
import os

class AIService:
    def __init__(self):
        self.endpoint = os.getenv('OLLAMA_ENDPOINT', 'http://ollama:11434')
    
    def explain(self, text, mode="teens"):
        prompt = f"""Explica esto para un adolescente usando una analogía divertida:
        Concepto: {text}
        """
        
        response = requests.post(
            f"{self.endpoint}/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False
            }
        )
        
        return response.json().get('response', 'Lo siento, no puedo explicarlo ahora.')