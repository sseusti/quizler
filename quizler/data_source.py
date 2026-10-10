"""Open Trivia Database integration."""

from typing import Any

import requests

from .models import Question

API_URL = "https://opentdb.com/api.php"
QUESTION_COUNT = 10


class QuestionSourceError(RuntimeError):
    """Raised when questions cannot be fetched or parsed."""


class OpenTriviaDataSource:
    def __init__(self, question_count: int = QUESTION_COUNT) -> None:
        self.question_count = question_count

    def fetch_questions(self) -> list[Question]:
        try:
            response = requests.get(
                API_URL,
                params={"amount": self.question_count, "type": "boolean"},
                timeout=10,
            )
            response.raise_for_status()
            payload: Any = response.json()
            results = payload["results"]
            questions = [
                Question.from_api(item["question"], item["correct_answer"])
                for item in results
            ]
        except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
            raise QuestionSourceError("Could not load questions from Open Trivia DB") from exc

        if not questions:
            raise QuestionSourceError("Open Trivia DB returned no questions")
        return questions
