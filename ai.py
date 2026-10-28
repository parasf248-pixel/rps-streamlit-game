"""Computer move strategies for Rock, Paper, Scissors."""

from __future__ import annotations

import random
from collections import Counter, defaultdict
from collections.abc import Sequence
from enum import Enum

from game import Move


class Difficulty(str, Enum):
    """Available computer strategies."""

    EASY = "Easy"
    MEDIUM = "Medium"
    SMART = "Smart"


_COUNTERS = {
    Move.ROCK: Move.PAPER,
    Move.PAPER: Move.SCISSORS,
    Move.SCISSORS: Move.ROCK,
}
_ALL_MOVES = tuple(Move)


def choose_computer_move(
    difficulty: Difficulty,
    player_history: Sequence[Move],
    rng: random.Random | None = None,
) -> Move:
    """Choose a move using the selected strategy and previous player moves."""
    if not isinstance(difficulty, Difficulty):
        raise ValueError("difficulty must be a Difficulty value.")
    if any(not isinstance(move, Move) for move in player_history):
        raise ValueError("Player history must contain only Move values.")

    random_source = rng if rng is not None else random.Random()
    if difficulty == Difficulty.EASY or not player_history:
        return random_source.choice(_ALL_MOVES)
    if difficulty == Difficulty.MEDIUM:
        return _choose_medium(player_history[-1], random_source)
    return _choose_smart(player_history, random_source)


def _choose_medium(last_move: Move, rng: random.Random) -> Move:
    if rng.random() < 0.65:
        return _COUNTERS[last_move]
    return rng.choice(_ALL_MOVES)


def _choose_smart(player_history: Sequence[Move], rng: random.Random) -> Move:
    transition_counts: dict[Move, Counter[Move]] = defaultdict(Counter)
    for previous_move, next_move in zip(
        player_history, player_history[1:], strict=False
    ):
        transition_counts[previous_move][next_move] += 1

    next_moves = transition_counts[player_history[-1]]
    if next_moves:
        most_likely = max(next_moves.values())
        likely_player_moves = [
            move for move, count in next_moves.items() if count == most_likely
        ]
    else:
        frequencies = Counter(player_history)
        most_likely = max(frequencies.values())
        likely_player_moves = [
            move for move, count in frequencies.items() if count == most_likely
        ]

    prediction = rng.choice(likely_player_moves)
    return _COUNTERS[prediction]
