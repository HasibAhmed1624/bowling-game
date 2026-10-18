# Plan — Bowling Game Kata (London Style)

Each numbered cycle below is executed by one invocation of the `tdd-step`
skill (red → green → refactor → stop). Tick a box when its cycle is done.

## Approach: Outside-in (top-down / mockist)

Start at the public API (`Game`), write one behavior test at a time, and push
responsibility into collaborators only when a failing test forces it. No
collaborator is created "just in case" — each one is born from a Game-level
test that can't be satisfied by the existing structure.

Bottom-up (build `Frame`/`Roll` classes first, then `Game`) is the classic
state-school path for this kata; we're deliberately not doing it.

Rule of thumb: mock at the boundary of the object under test and verify
interactions there; once a collaborator exists, its own tests can be plain
state-based tests (mock nothing below the boundary).

## Public API (fixed by requirements.md)

- `Game.roll(pins: int) -> None`
- `Game.score() -> int`

## Test list (ordered)

Each row = one red-green-refactor cycle via `/tdd-step`.

| # | Done | Test (Game level) | Expectation | Likely collaborator born here |
|---|------|-------------------|-------------|-------------------------------|
| 1 | [x] | gutter game: 20 rolls of 0 | score 0 | none — Game keeps a raw roll log |
| 2 | [x] | all ones: 20 rolls of 1 | score 20 | — |
| 3 | [x] | frame completes after 2 rolls (1 if strike) | frame counter advances | `Frame` (rolls, `is_complete()`, bonus length) |
| 4 | [x] | spare, then next roll is 3 | spare frame scores 13 | `Frame` gains spare bonus lookup |
| 5 | [ ] | strike, then next two rolls | strike frame scores 10 + next two | `Frame` gains strike bonus |
| 6 | [ ] | 10th-frame spare → one extra roll counts | total includes bonus roll | `Frames` (10-frame boundary rules) |
| 7 | [ ] | 10th-frame strike → two extra rolls | total includes both | `Frames` handles overflow rolls |
| 8 | [ ] | perfect game: 12 strikes | 300 | integration check across collaborators |
| 9 | [ ] | all spares: 21 rolls of 5 | 150 | optional safety net |

The "collaborator born here" column is a forecast, not a spec — let the
failures tell you. A cycle may just deepen an existing collaborator instead.

## Expected emergent design (not fixed upfront)

```
Game                # facade: roll(), score(); delegates everything
├─ RollLog          # raw ordered pins (may stay a plain list inside Game)
├─ Frame            # one frame: rolls, is_complete(), pins, bonus length
└─ Frames           # splits roll stream into 10 frames + 10th-frame extras
                    # scoring may live here or in a tiny ScoreCalculator
```

Do not create these on day one. They appear when a test demands them.

## Session rhythm

1. Pick the next row from the test list.
2. Write the failing test (mock collaborators that don't exist yet → import
   error or interaction failure is fine; that's the red).
3. Implement the minimum: create/stub collaborators, wire them into `Game`.
4. Green. Refactor with all tests running.
5. Repeat.

## GUI (after the core is green)

Tkinter scorecard: frame grid, roll entry buttons, running total. `Game` stays
UI-agnostic, so the GUI is a thin adapter — no TDD cycles required, but it's a
good manual feedback loop and demo.
