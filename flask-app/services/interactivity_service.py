import subprocess
import json

class InteractivityService:
    def validate_python_code(self, code: str, expected_output: str) -> dict:
        try:
            process = subprocess.run(
                ["python3", "-c", f"{code}\nprint(mi_perro)"],
                capture_output=True,
                text=True,
                timeout=10
            )
            output = process.stdout.strip()
            return {
                "is_correct": output == expected_output,
                "user_output": output,
                "expected_output": expected_output
            }
        except Exception as e:
            return {"error": str(e)}