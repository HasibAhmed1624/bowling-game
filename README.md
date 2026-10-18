# Bowling Game Kata

Bowling Game Kata ([kata-log.rocks](https://kata-log.rocks/bowling-game-kata)) done with **outside-in TDD** in Python, plus a two-player **Tkinter** demo GUI. See [requirements.md](requirements.md) for the rules and the implemented API.

## Stack

- **Python 3.10+** with `src/` layout
- **pytest** — state-based unit tests (no mocks; `pytest-mock` is intentionally not a dependency)
- **pytest-watch** — continuous test runs during TDD (`ptw`)
- **pytest-cov** — coverage runs by default; `gui/app.py` (thin Tk adapter) is omitted
- **Tkinter** — stdlib GUI (separate package on some distros)

## Setup

Using [uv](https://docs.astral.sh/uv/) (recommended):

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
.venv/bin/pytest     # single run (43 tests) + coverage report
.venv/bin/ptw        # continuous TDD loop
```

Coverage config lives in `pyproject.toml` (`[tool.coverage.*]`); runs report
missing lines and enforce a floor. The Tk GUI itself is excluded — only its pure
logic (`gui/logic.py`) is measured.

## Running the GUI

```sh
python -m bowling_game.gui
```

Two scripted players, Ada (129) and Grace (198), play ball by ball so the
scoring is visible:

- **Next roll** advances one ball (players alternate); **Play** auto-plays; **Reset** restarts.
- Frame cells show notation (`X` strike, `/` spare, `-` zero) and the cumulative
  total once a frame is finalized — that is why the total appears only after the
  frame's bonus balls have landed.
- The log explains each ball ("STRIKE. Scores 10 + the next two rolls") and each
  finalized frame (`Ada frame 1 final: X → 19 pins`).
- The scripted games and pure display helpers live in `gui/logic.py`, unit-tested.

## Layout

```
src/bowling_game/
  game.py        # Game: thin facade over Frames
  frames.py      # Frames: roll log, 10-frame cap, scoring walk
  frame.py       # Frame: one frame's rolls, completion, spare/strike
  gui/logic.py   # scripted series, marks, cumulatives, narration (pure, tested)
  gui/app.py     # Tkinter scorecard (thin adapter, excluded from coverage)
  gui/__main__.py
tests/
  test_game.py       # Game-level behavior
  test_frames.py     # Frames behavior + scoring breakdown
  test_frame.py      # Frame state predicates
  test_gui_logic.py  # series, notation, cumulatives, narration
```

## TDD approach (what actually happened)

The plan in [plan.md](plan.md) lists the intended cycles; the honest record is:

- **Outside-in.** `Game` started as a raw roll log; `Frame` and `Frames` were
  born only when a failing test demanded them. No collaborator was created
  because a plan forecast it.
- **State-based, not mock-based.** London-style intent, but every test asserts
  observable behavior; no test doubles are used.
- **5 of the 9 planned rows never went red.** Gutter/all-ones and the 10th-frame
  and full-game rows were already satisfied by earlier structure; they are kept
  as regression tests. The real reds were frame counting (step 3), the spare
  bonus (step 4), and the strike bonus (step 5).
- **The GUI forced the interesting work**: partial-safe `score()`, the
  `frame_scores()` breakdown, and a real bug in `Frame.is_complete` (three-roll
  tenth frames), all discovered when the view consumed a game in progress.

The reusable workflow lives in the personal skills `tdd-test-finder` (derive the
test list from the state space), `tdd-plan` (discriminable rows), and
`tdd-step` (one red-green-refactor cycle per invocation).
