"""Application composition and startup error handling."""

import tkinter as tk
from tkinter import messagebox

from .data_source import OpenTriviaDataSource, QuestionSourceError
from .models import Quiz
from .ui import QuizWindow


def main() -> None:
    try:
        questions = OpenTriviaDataSource().fetch_questions()
    except QuestionSourceError as exc:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Unable to start quiz", str(exc), parent=root)
        root.destroy()
        return

    QuizWindow(Quiz(questions)).run()
