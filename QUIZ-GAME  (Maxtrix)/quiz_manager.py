import json
import random
import os

class QuizManager:
    def __init__(self, category="general"):
        """
        category: nom du dossier de catégorie (ex: 'Python', 'C', 'Culture_generale')
        """
        self.category = category
        self.questions_path = os.path.join("data", "questions", self.category)
        self.levels = ["easy", "medium", "hard"]
        os.makedirs(self.questions_path, exist_ok=True)

        
        for level in self.levels:
            file_path = os.path.join(self.questions_path, f"{level}.json")
            if not os.path.exists(file_path):
                default_questions = {
                    "questions": [
                        {
                            "id": i + 1,
                            "question": f"Example question {level} {i + 1}",
                            "options": [f"Option {j + 1}" for j in range(4)],
                            "correct_answer": random.randint(0, 3),
                            "difficulty": level,
                            "category": self.category,
                            "explanation": f"Explanation for question {level} {i + 1}"
                        }
                        for i in range(10)
                    ]
                }
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(default_questions, f, indent=4, ensure_ascii=False)

    def load_questions(self, level):
        """
        level: 'easy', 'medium' ou 'hard'
        Retourne la liste des questions pour la catégorie et le niveau choisis.
        """
        file_path = os.path.join(self.questions_path, f"{level}.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("questions", [])
        except FileNotFoundError:
            return []

    def get_random_question(self, level):
        questions = self.load_questions(level)
        if not questions:
            return None
        return random.choice(questions)

    def verify_answer(self, question, answer_index):
        return question.get("correct_answer") == answer_index
