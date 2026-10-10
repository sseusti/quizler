import unittest

from quizler.models import Question, Quiz


class QuestionTests(unittest.TestCase):
    def test_from_api_normalizes_answer_and_unescapes_text(self) -> None:
        question = Question.from_api("Cats &amp; dogs", "TRUE")

        self.assertEqual(question.text, "Cats & dogs")
        self.assertIs(question.answer, True)

    def test_from_api_rejects_non_boolean_answers(self) -> None:
        with self.assertRaises(ValueError):
            Question.from_api("Question", "sometimes")


class QuizTests(unittest.TestCase):
    def setUp(self) -> None:
        self.questions = [Question("First", True), Question("Second", False)]
        self.quiz = Quiz(self.questions)

    def test_rejects_empty_question_list(self) -> None:
        with self.assertRaises(ValueError):
            Quiz([])

    def test_tracks_progress_and_score(self) -> None:
        self.assertTrue(self.quiz.has_questions)
        self.assertEqual(self.quiz.next_question(), self.questions[0])
        self.assertTrue(self.quiz.submit_answer(True))
        self.assertEqual(self.quiz.score, 1)

        self.assertEqual(self.quiz.next_question(), self.questions[1])
        self.assertFalse(self.quiz.submit_answer(True))
        self.assertEqual(self.quiz.score, 1)
        self.assertFalse(self.quiz.has_questions)
        self.assertEqual(self.quiz.answered_questions, 2)

    def test_rejects_answer_without_active_question(self) -> None:
        with self.assertRaises(RuntimeError):
            self.quiz.submit_answer(True)

    def test_rejects_answering_a_question_twice(self) -> None:
        self.quiz.next_question()
        self.quiz.submit_answer(True)

        with self.assertRaises(RuntimeError):
            self.quiz.submit_answer(True)

    def test_rejects_request_after_last_question(self) -> None:
        self.quiz.next_question()
        self.quiz.submit_answer(True)
        self.quiz.next_question()
        self.quiz.submit_answer(False)

        with self.assertRaises(StopIteration):
            self.quiz.next_question()

    def test_reset_starts_a_fresh_session(self) -> None:
        self.quiz.next_question()
        self.quiz.submit_answer(True)
        self.quiz.next_question()
        self.quiz.submit_answer(False)

        self.quiz.reset()

        self.assertTrue(self.quiz.has_questions)
        self.assertEqual(self.quiz.score, 0)
        self.assertEqual(self.quiz.answered_questions, 0)
        self.assertIsNone(self.quiz.current_question)
        self.assertEqual(self.quiz.next_question(), self.questions[0])


if __name__ == "__main__":
    unittest.main()
