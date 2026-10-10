"""Core quiz types, independent of the user interface and data source."""

from dataclasses import dataclass
import html


@dataclass(frozen=True)
class Question:
    """A true/false question and its expected answer."""

    text: str
    answer: bool

    @classmethod
    def from_api(cls, text: str, answer: str) -> "Question":
        normalized = answer.strip().lower()
        if normalized not in {"true", "false"}:
            raise ValueError(f"Expected a true/false answer, got {answer!r}")
        return cls(text=html.unescape(text), answer=normalized == "true")


class Quiz:
    """Tracks progress and scoring for a single quiz session."""

    def __init__(self, questions: list[Question]) -> None:
        if not questions:
            raise ValueError("A quiz needs at least one question")
        self._questions = tuple(questions)
        self._position = 0
        self.score = 0
        self._has_answered_current = False

    @property
    def total_questions(self) -> int:
        return len(self._questions)

    @property
    def answered_questions(self) -> int:
        return self._position

    @property
    def current_question(self) -> Question | None:
        if self._position == 0 or self._position > len(self._questions):
            return None
        return self._questions[self._position - 1]

    @property
    def has_questions(self) -> bool:
        return self._position < len(self._questions)

    def next_question(self) -> Question:
        if not self.has_questions:
            raise StopIteration("The quiz is complete")
        question = self._questions[self._position]
        self._position += 1
        self._has_answered_current = False
        return question

    def submit_answer(self, answer: bool) -> bool:
        question = self.current_question
        if question is None:
            raise RuntimeError("There is no active question to answer")
        if self._has_answered_current:
            raise RuntimeError("The current question has already been answered")
        self._has_answered_current = True
        is_correct = answer is question.answer
        if is_correct:
            self.score += 1
        return is_correct

    def reset(self) -> None:
        """Start the same quiz again from its first question."""
        self._position = 0
        self.score = 0
        self._has_answered_current = False
