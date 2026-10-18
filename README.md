# Bowling Game Kata

Bowling Game Kata ([kata-log.rocks](https://kata-log.rocks/bowling-game-kata)) done with **London-style TDD** in Python, plus an optional **Tkinter** GUI. See [requirements.md](requirements.md) for the kata rules.

## Stack

- **Python 3.10+** with `src/` layout
- **pytest** + **pytest-mock** — London style leans on interaction tests and test doubles (`mocker` fixture)
- **pytest-watch** — continuous test runs during TDD
- **Tkinter** — stdlib GUI (no extra install on most distros)

## Setup

Using [uv](https://docs.astral.sh/uv/) (recommended; already on PATH here):

```sh
uv venv .venv
uv pip install --python .venv/bin/python -e ".[dev]"
```

Or with a plain venv (requires `python3-venv` / `python3-pip`):

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Tkinter ships with the standard library but is a separate package on some distros. On Debian/Ubuntu:

```sh
sudo apt install python3-tk
```

## Running tests

```sh
.venv/bin/pytest                              # single run
.venv/bin/ptw                                 # continuous TDD loop
```

## Running the GUI (once it exists)

```sh
python -m bowling_game.gui
```

## Layout

```
src/bowling_game/        # production code (Game class, collaborators)
src/bowling_game/gui/    # Tkinter UI
tests/                   # pytest tests, one collaborator at a time
```

## TDD (London style) approach

`Game` has no collaborators by default, so the London style means deliberately introducing and mocking them (e.g. `RollTracker`, `Frame`, `ScoreCalculator`) and driving them one at a time through interaction tests. Each red-green-refactor cycle: write a failing mock-based test, implement the minimum, refactor with both unit tests and the GUI as a feedback loop.
