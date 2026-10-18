import tkinter as tk
from tkinter import ttk

from bowling_game.game import Game
from bowling_game.gui.logic import PLAYER_SERIES, cumulatives, expand_series, marks

ROLL_DELAY_MS = 700


class BowlingApp:
    """Two scripted players, played roll by roll so you can follow the scoring."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Bowling Game — two-player demo")
        self.series = {name: expand_series(spec) for name, spec in PLAYER_SERIES.items()}
        self.games = {name: Game() for name in self.series}
        self.cursor = {name: 0 for name in self.series}
        self.prev_scores: dict[str, list[int | None]] = {name: [] for name in self.series}
        self._turn = 0
        self.playing = False
        self._after_id: str | None = None

        self.frame_cells: dict[str, list[tuple[ttk.Label, ttk.Label]]] = {}
        self.total_labels: dict[str, ttk.Label] = {}

        self._build()
        self._log("Press 'Next roll' to advance one ball, or 'Play' to watch the whole game.")
        self._refresh()

    def _build(self) -> None:
        self.root.columnconfigure(0, weight=1)
        ttk.Label(
            self.root,
            text="Two scripted players — watch how strikes and spares pay off",
            font=("TkDefaultFont", 12, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 6))

        row = 1
        for name in self.series:
            panel = ttk.LabelFrame(self.root, text=name)
            panel.grid(row=row, column=0, sticky="ew", padx=10, pady=4)
            cells: list[tuple[ttk.Label, ttk.Label]] = []
            for frame_index in range(10):
                cell = ttk.Frame(panel, relief="ridge", borderwidth=1, padding=2)
                cell.grid(row=0, column=frame_index, padx=1, pady=2)
                ttk.Label(cell, text=str(frame_index + 1), font=("TkDefaultFont", 8, "bold")).grid(row=0, column=0)
                rolls_label = ttk.Label(cell, text="", width=6, anchor="center")
                rolls_label.grid(row=1, column=0)
                score_label = ttk.Label(cell, text="", width=6, anchor="center", foreground="#0a6")
                score_label.grid(row=2, column=0)
                cells.append((rolls_label, score_label))
            self.frame_cells[name] = cells
            total = ttk.Label(panel, text="Total: 0", font=("TkDefaultFont", 11, "bold"))
            total.grid(row=0, column=10, padx=10)
            self.total_labels[name] = total
            row += 1

        controls = ttk.Frame(self.root)
        controls.grid(row=row, column=0, sticky="w", padx=10, pady=(6, 2))
        row += 1
        self.next_button = ttk.Button(controls, text="Next roll", command=self._step)
        self.next_button.grid(row=0, column=0, padx=(0, 6))
        self.play_button = ttk.Button(controls, text="Play", command=self._toggle_play)
        self.play_button.grid(row=0, column=1, padx=6)
        ttk.Button(controls, text="Reset", command=self._reset).grid(row=0, column=2, padx=6)

        log_frame = ttk.LabelFrame(self.root, text="What just happened")
        log_frame.grid(row=row, column=0, sticky="nsew", padx=10, pady=(4, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        self.root.rowconfigure(row, weight=1)
        self.log = tk.Text(log_frame, height=9, width=90, wrap="word", state="disabled")
        self.log.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_frame, command=self.log.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log.configure(yscrollcommand=scrollbar.set)

    def _active_players(self) -> list[str]:
        return [name for name in self.series if self.cursor[name] < len(self.series[name])]

    def _step(self) -> None:
        active = self._active_players()
        if not active:
            self._stop_play()
            self._log("Game over — press Reset to replay.")
            return
        name = active[self._turn % len(active)]
        self._turn += 1
        self._roll_for(name)

    def _roll_for(self, name: str) -> None:
        pins = self.series[name][self.cursor[name]]
        self.cursor[name] += 1
        game = self.games[name]
        game.roll(pins)
        self._explain(name, pins)
        self._refresh()

    def _explain(self, name: str, pins: int) -> None:
        game = self.games[name]
        frame_number = game.frame_number
        rolls_per_frame = game.rolls_per_frame
        frame = rolls_per_frame[frame_number - 1] if frame_number - 1 < len(rolls_per_frame) else ()

        if pins == 10:
            self._log(f"{name} — frame {frame_number}: STRIKE. Scores 10 + the next two rolls.")
        else:
            self._log(f"{name} — frame {frame_number}: rolled {pins}.")
        if len(frame) == 2 and sum(frame) == 10:
            self._log(f"    spare! this frame scores 10 + the next roll.")

        previous = self.prev_scores[name]
        for index, score in enumerate(game.frame_scores()):
            was = previous[index] if index < len(previous) else None
            if score is not None and was is None:
                notation = " ".join(marks(rolls_per_frame[index]))
                self._log(f"    frame {index + 1} final: {notation} → {score} pins")
        self.prev_scores[name] = game.frame_scores()

    def _refresh(self) -> None:
        for name, game in self.games.items():
            cumulative = cumulatives(game.frame_scores())
            rolls_per_frame = game.rolls_per_frame
            for index, (rolls_label, score_label) in enumerate(self.frame_cells[name]):
                notation = marks(rolls_per_frame[index]) if index < len(rolls_per_frame) else []
                rolls_label.configure(text=" ".join(notation))
                total = cumulative[index] if index < len(cumulative) else None
                score_label.configure(text="" if total is None else str(total))
            self.total_labels[name].configure(text=f"Total: {game.score()}")
        self.next_button.configure(state="normal" if self._active_players() else "disabled")

    def _toggle_play(self) -> None:
        if self.playing:
            self._stop_play()
        else:
            self.playing = True
            self.play_button.configure(text="Pause")
            self._play_tick()

    def _play_tick(self) -> None:
        if not self.playing:
            return
        if not self._active_players():
            self._stop_play()
            self._log("Both players finished.")
            return
        self._step()
        self._after_id = self.root.after(ROLL_DELAY_MS, self._play_tick)

    def _stop_play(self) -> None:
        self.playing = False
        self.play_button.configure(text="Play")
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
            self._after_id = None

    def _reset(self) -> None:
        self._stop_play()
        self.games = {name: Game() for name in self.series}
        self.cursor = {name: 0 for name in self.series}
        self.prev_scores = {name: [] for name in self.series}
        self._turn = 0
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
        self._log("Fresh game — press 'Next roll' or 'Play'.")
        self._refresh()

    def _log(self, message: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")


def main() -> None:
    root = tk.Tk()
    BowlingApp(root)
    root.mainloop()
