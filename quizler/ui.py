"""Tkinter presentation layer for a quiz session."""

from pathlib import Path
import tkinter as tk

from .models import Quiz

THEME_COLOR = "#375362"
ROOT_DIR = Path(__file__).resolve().parent.parent


class QuizWindow:
    def __init__(self, quiz: Quiz) -> None:
        self.quiz = quiz
        self.root = tk.Tk()
        self.root.title("Quizzler")
        self.root.configure(bg=THEME_COLOR, padx=20, pady=20)
        self.root.resizable(False, False)

        self.score_label = tk.Label(
            self.root, text="Score: 0", fg="white", bg=THEME_COLOR,
            font=("Arial", 12, "bold"),
        )
        self.score_label.grid(row=0, column=1, sticky="e")

        self.canvas = tk.Canvas(
            self.root, width=320, height=250, bg="white", highlightthickness=0,
        )
        self.question_text = self.canvas.create_text(
            160, 125, text="", width=285, font=("Arial", 18, "italic"),
            fill=THEME_COLOR, justify="center",
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=24)

        self._true_image = tk.PhotoImage(file=str(ROOT_DIR / "images" / "true.png"))
        self._false_image = tk.PhotoImage(file=str(ROOT_DIR / "images" / "false.png"))
        self.true_button = tk.Button(
            self.root, image=self._true_image, command=lambda: self._submit(True),
            highlightthickness=0, borderwidth=0,
        )
        self.false_button = tk.Button(
            self.root, image=self._false_image, command=lambda: self._submit(False),
            highlightthickness=0, borderwidth=0,
        )
        self.true_button.grid(row=2, column=0, padx=12)
        self.false_button.grid(row=2, column=1, padx=12)

        self._show_next_question()

    def run(self) -> None:
        self.root.mainloop()

    def _show_next_question(self) -> None:
        self.canvas.configure(bg="white")
        self.true_button.configure(state=tk.NORMAL)
        self.false_button.configure(state=tk.NORMAL)
        self.score_label.configure(text=f"Score: {self.quiz.score}")

        if not self.quiz.has_questions:
            self.canvas.itemconfigure(
                self.question_text,
                text=f"Quiz complete!\nFinal score: {self.quiz.score}/{self.quiz.total_questions}",
            )
            self.true_button.configure(state=tk.DISABLED)
            self.false_button.configure(state=tk.DISABLED)
            return

        question = self.quiz.next_question()
        self.canvas.itemconfigure(
            self.question_text,
            text=f"Question {self.quiz.answered_questions}/{self.quiz.total_questions}\n\n{question.text}",
        )

    def _submit(self, answer: bool) -> None:
        is_correct = self.quiz.submit_answer(answer)
        self.true_button.configure(state=tk.DISABLED)
        self.false_button.configure(state=tk.DISABLED)
        self.canvas.configure(bg="#3b9b62" if is_correct else "#d9534f")
        self.root.after(800, self._show_next_question)
