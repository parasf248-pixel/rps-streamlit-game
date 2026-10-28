"""Tests for the computer's difficulty strategies."""

import random

import pytest

from ai import Difficulty, choose_computer_move
from game import Move


class FirstMoveRandom(random.Random):
    """A predictable random source for strategy tests."""

    def random(self):
        return 0.0

    def choice(self, sequence):
        return sequence[0]


class RandomBranchSource(FirstMoveRandom):
    def random(self):
        return 0.99


@pytest.mark.parametrize("difficulty", list(Difficulty))
def test_strategies_choose_a_valid_move_without_history(difficulty):
    move = choose_computer_move(difficulty, [], rng=FirstMoveRandom())
    assert move in Move


def test_easy_chooses_from_all_moves():
    assert (
        choose_computer_move(Difficulty.EASY, [Move.ROCK], rng=FirstMoveRandom())
        == Move.ROCK
    )


@pytest.mark.parametrize(
    ("last_move", "expected"),
    [
        (Move.ROCK, Move.PAPER),
        (Move.PAPER, Move.SCISSORS),
        (Move.SCISSORS, Move.ROCK),
    ],
)
def test_medium_counters_last_move_most_of_the_time(last_move, expected):
    assert (
        choose_computer_move(Difficulty.MEDIUM, [last_move], rng=FirstMoveRandom())
        == expected
    )


def test_medium_sometimes_chooses_randomly():
    move = choose_computer_move(
        Difficulty.MEDIUM,
        [Move.ROCK],
        rng=RandomBranchSource(),
    )
    assert move == Move.ROCK


def test_smart_uses_move_transition_pattern():
    history = [Move.ROCK, Move.PAPER, Move.ROCK, Move.PAPER, Move.ROCK]
    # After Rock the player repeatedly chose Paper, so the computer counters Paper.
    assert (
        choose_computer_move(Difficulty.SMART, history, rng=FirstMoveRandom())
        == Move.SCISSORS
    )


def test_smart_falls_back_to_overall_frequencies():
    history = [Move.ROCK, Move.PAPER, Move.PAPER]
    # Paper is the most common move, and Scissors beats Paper.
    assert (
        choose_computer_move(Difficulty.SMART, history, rng=FirstMoveRandom())
        == Move.SCISSORS
    )


def test_smart_uses_random_tie_break_between_likely_moves():
    history = [Move.ROCK, Move.PAPER, Move.ROCK, Move.SCISSORS, Move.ROCK]
    assert (
        choose_computer_move(Difficulty.SMART, history, rng=FirstMoveRandom())
        == Move.SCISSORS
    )


def test_strategy_rejects_invalid_difficulty_and_history():
    with pytest.raises(ValueError, match="difficulty"):
        choose_computer_move("hard", [])
    with pytest.raises(ValueError, match="history"):
        choose_computer_move(Difficulty.EASY, ["rock"])
