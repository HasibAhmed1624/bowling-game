# Bowling Game Kata

## Source
https://kata-log.rocks/bowling-game-kata

## Rules

The game consists of 10 frames. In each frame the player has two rolls to knock down 10 pins. The score for the frame is the total number of pins knocked down, plus bonuses for strikes and spares.

### Scoring

**Spare**: When the player knocks down all 10 pins in two rolls.
- The bonus for that frame is the number of pins knocked down by the **next roll** only.

**Strike**: When the player knocks down all 10 pins on his first roll.
- The frame is then completed with a single roll (no second roll in that frame).
- The bonus for that frame is the value of the **next two rolls**.

### Tenth Frame
A player who rolls a spare or strike in the tenth frame is allowed to roll extra balls to complete the frame. However, no more than three balls can be rolled in the tenth frame.

## Requirements

Write a class `Game` that has two methods:

- `void roll(int pins)` - called each time the player rolls a ball. The argument is the number of pins knocked down.
- `int score()` - returns the total score for that game.

### API

The kata contract above is the required public API. The implementation also
exposes these read-only accessors, added because the scorecard GUI is a consumer
of a game in progress:

| Member | Type | Meaning |
|--------|------|---------|
| `Game.frame_number` | `int` | Current frame, `1..10` (capped at 10 during the tenth frame). |
| `Game.rolls_per_frame` | `list[tuple[int, ...]]` | The balls rolled so far, grouped per frame; the last tuple may be empty or partial. |
| `Game.frame_scores()` | `list[int \| None]` | Score of each frame, or `None` while its bonus rolls have not all been rolled. |

### Scoring a game in progress

`score()` (and `frame_scores()`) may be called at any point, not only when the
game is over:

- Only **finalized** frames are counted — a frame finalizes once all of its
  bonus rolls (two for a strike, one for a spare, none for an open frame) have
  been rolled.
- A partially rolled open frame contributes nothing yet.
- `score()` never raises for an incomplete game; it returns the total of the
  finalized frames.

### Explicitly unsupported

Not validated by design: pin values outside `0..10`, illegal sequences (e.g. a
third ball in a non-tenth frame), and rolls after the game is over (extra rolls
are appended to the tenth frame). The caller is responsible for legal input.