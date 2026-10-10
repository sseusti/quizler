# Quizzler

A true-or-false desktop quiz built with Python and Tkinter. The app fetches questions from the [Open Trivia Database](https://opentdb.com/), displays them in a graphical window, and keeps track of the score.

## Features

- A graphical interface built with Tkinter, without third-party UI frameworks.
- True/false questions fetched from the Open Trivia Database.
- Visual feedback for each answer through the question card's background color.
- A running score and a final result at the end of the quiz.
- Startup handling for network errors and invalid API responses.

## Tkinter interface

The main window is implemented by `QuizWindow` in `quizler/ui.py`. It uses standard Tkinter widgets: `Tk` for the application window, `Canvas` for the question card, `Label` for the score, and `Button` widgets for the answers. Button images are stored in `images/`.

The answer buttons are connected to event handlers through their `command` callbacks. After an answer is submitted, the interface disables both buttons, changes the card color, and schedules the next question with `root.after`. This keeps the short feedback delay from blocking Tkinter's event loop. The `mainloop` is started separately by `run()`.

## Architecture

The code is organized by responsibility: the UI handles presentation and events, the model tracks quiz state, and the data source handles API communication.

```text
main.py                  Application entry point
quizler/
  app.py                 Application setup and loading error handling
  data_source.py         Open Trivia Database request and response validation
  models.py              Question and Quiz session logic
  ui.py                  Tkinter window and user interaction handlers
images/                  True / False button artwork
requirements.txt         Python dependencies
```

At startup, `app.py` fetches the questions, creates a `Quiz` session, and passes it to `QuizWindow`. The model has no Tkinter dependency, and the UI does not handle HTTP details. The API request runs when the app starts, rather than when modules are imported.

## Requirements

- Python 3.10 or newer.
- Tkinter available in your Python installation.
- Internet access to fetch questions.

Tkinter is included with many Python distributions. On some Linux systems, it may need to be installed as a separate system package.

## Installation and run

From the project root, run:

```bash
python -m pip install -r requirements.txt
python main.py
```

If the API cannot be reached, the app displays an error message and exits. Once the questions load, answer them in the quiz window.

## Question source

Questions are fetched over HTTPS from the Open Trivia Database. The question count and type are configured in `quizler/data_source.py`. The app uses `requests` for HTTP; the remaining components rely on the Python standard library.
