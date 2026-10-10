# Quizzler

A small true/false quiz desktop app built with Python and Tkinter. Questions are
loaded from the [Open Trivia Database](https://opentdb.com/).

## Run

Install the dependency with `python -m pip install -r requirements.txt`, then run:

```bash
python main.py
```

## Structure

- `main.py` is the executable entry point.
- `quizler/app.py` wires the data source, quiz session, and window together.
- `quizler/data_source.py` handles the Open Trivia Database request and response validation.
- `quizler/models.py` contains question and quiz-session logic without UI dependencies.
- `quizler/ui.py` contains the Tkinter presentation and user interactions.
- `images/` contains the answer button artwork.

Network access is used only when the app starts, rather than when modules are imported.
