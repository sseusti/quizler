# Quizzler

Quizzler is a small true-or-false desktop quiz built with Python and Tkinter. It fetches questions from the [Open Trivia Database](https://opentdb.com/) and presents them in an interactive window.

## Features

- True-or-false questions loaded from the Open Trivia Database.
- Answer using the on-screen buttons or the keyboard: **Left Arrow = True**, **Right Arrow = False**.
- Immediate visual feedback: the question card changes color after an answer.
- Hover feedback on answer buttons and a live score display.
- A final score and a **Play again** button to replay the same set of questions.
- Protection against submitting multiple answers to the same question.
- A startup error message if the API request fails or returns invalid data.

## Tkinter interface

The graphical interface lives in `quizler/ui.py` and is built from standard Tkinter widgets:

- `Tk` creates the application window.
- `Canvas` displays the current question and answer feedback.
- `Label` displays the score.
- `Button` widgets provide True, False, and Play again actions.

Button `command` callbacks and window key bindings handle user input. After an answer, the buttons are disabled and `root.after` schedules the next question after a brief pause. This keeps the interface responsive by letting Tkinter's event loop continue running. `mainloop()` is started by `QuizWindow.run()`.

## Architecture

The project keeps the interface, quiz rules, and API integration in separate modules:

```text
main.py                  Application entry point
quizler/
  app.py                 Application setup and startup error handling
  data_source.py         Open Trivia Database client and response validation
  models.py              Question type and quiz session state
  ui.py                  Tkinter window, widgets, and event handlers
images/                  True / False button artwork
tests/
  test_models.py         Unit tests for question and quiz behavior
requirements.txt         Python dependencies
```

At startup, `app.py` asks `OpenTriviaDataSource` for questions, creates a `Quiz` session, and passes it to `QuizWindow`. The model has no Tkinter dependency, while the UI does not make HTTP requests. Network access happens at startup rather than during module imports.

## Requirements

- Python 3.10 or newer.
- Tkinter available in your Python installation. Some Linux distributions package it separately.
- Internet access to fetch questions.

## Installation and run

From the project root, install the dependency and launch the app:

```bash
python -m pip install -r requirements.txt
python main.py
```

When the quiz opens, answer each question with a button or an arrow key. At the end, choose **Play again** to reset the score and start from the first question.

## Tests

The quiz model is covered by tests using Python's built-in `unittest` framework:

```bash
python -m unittest discover -s tests
```

## Question source

Questions are fetched over HTTPS from the Open Trivia Database. The number and type of questions are configured in `quizler/data_source.py`. `requests` is used for HTTP; the rest of the app uses the Python standard library and Tkinter.
