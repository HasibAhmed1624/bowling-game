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