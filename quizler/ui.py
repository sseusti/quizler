"""Tkinter presentation layer for a quiz session."""

from pathlib import Path
import tkinter as tk

from .models import Quiz

THEME_COLOR = "#375362"
CARD_COLOR = "#f7f9fa"
CORRECT_COLOR = "#3b9b62"
INCORRECT_COLOR = "#d9534f"
ROOT_DIR = Path(__file__).resolve().parent.parent


class QuizWindow:
    def __init__(self, quiz: Quiz) -> None:
        self.quiz = quiz
        self.root = tk.Tk()
        self.root.title("Quizzler")
        self.root.configure(bg=THEME_COLOR, padx=20, pady=20)
        self.root.resizable(False, False)
        self._answer_pending = False
        self.root.bind("<Left>", lambda _event: self._submit_from_key(True))
        self.root.bind("<Right>", lambda _event: self._submit_from_key(False))

        self.score_label = tk.Label(
            self.root, text="Score: 0", fg="white", bg=THEME_COLOR,
            font=("Arial", 12, "bold"),
        )
        self.score_label.grid(row=0, column=1, sticky="e")

        self.canvas = tk.Canvas(
            self.root, width=340, height=260, bg=CARD_COLOR, highlightthickness=0,
        )
        self.question_text = self.canvas.create_text(
            170, 130, text="", width=300, font=("Arial", 17, "italic"),
            fill=THEME_COLOR, justify="center",
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=24)

        self._true_image = tk.PhotoImage(file=str(ROOT_DIR / "images" / "true.png"))
        self._false_image = tk.PhotoImage(file=str(ROOT_DIR / "images" / "false.png"))
        self.true_button = tk.Button(
            self.root, image=self._true_image, command=lambda: self._submit(True),
            highlightthickness=0, borderwidth=0, cursor="hand2",
            activebackground=THEME_COLOR, takefocus=True,
        )
        self.false_button = tk.Button(
            self.root, image=self._false_image, command=lambda: self._submit(False),
            highlightthickness=0, borderwidth=0, cursor="hand2",
            activebackground=THEME_COLOR, takefocus=True,
        )
        self.true_button.grid(row=2, column=0, padx=12)
        self.false_button.grid(row=2, column=1, padx=12)
        self._add_hover_feedback(self.true_button)
        self._add_hover_feedback(self.false_button)
        self.restart_button = tk.Button(
            self.root, text="Play again", command=self._restart,
            font=("Arial", 10, "bold"), bg=CARD_COLOR, fg=THEME_COLOR,
            activebackground="white", activeforeground=THEME_COLOR,
            relief=tk.FLAT, cursor="hand2", padx=16, pady=8,
        )
        self.restart_button.grid(row=3, column=0, columnspan=2, pady=(18, 0))
        self.restart_button.grid_remove()

        self._show_next_question()

    def run(self) -> None:
        self.root.mainloop()

    def _show_next_question(self) -> None:
        self._answer_pending = True
        self.canvas.configure(bg=CARD_COLOR)
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
            self._answer_pending = False
            self.restart_button.grid()
            return

        question = self.quiz.next_question()
        self.canvas.itemconfigure(
            self.question_text,
            text=f"Question {self.quiz.answered_questions}/{self.quiz.total_questions}\n\n{question.text}",
        )

    def _submit(self, answer: bool) -> None:
        if not self._answer_pending:
            return
        self._answer_pending = False
        is_correct = self.quiz.submit_answer(answer)
        self.true_button.configure(state=tk.DISABLED)
        self.false_button.configure(state=tk.DISABLED)
        self.canvas.configure(bg=CORRECT_COLOR if is_correct else INCORRECT_COLOR)
        self.root.after(800, self._show_next_question)

    def _submit_from_key(self, answer: bool) -> str:
        self._submit(answer)
        return "break"

    @staticmethod
    def _add_hover_feedback(button: tk.Button) -> None:
        button.bind(
            "<Enter>",
            lambda _event: button.configure(relief=tk.RAISED, borderwidth=2),
        )
        button.bind(
            "<Leave>",
            lambda _event: button.configure(relief=tk.FLAT, borderwidth=0),
        )

    def _restart(self) -> None:
        self.restart_button.grid_remove()
        self.quiz.reset()
        self._show_next_question()
