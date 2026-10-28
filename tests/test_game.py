"""Tests for game rules and match scoring."""

import pytest

from game import (
    Move,
    Outcome,
    RoundResult,
    calculate_score,
    create_round_result,
    determine_outcome,
    match_outcome,
    validate_best_of,
)


@pytest.mark.parametrize(
    ("player", "computer", "expected"),
    [
        (Move.ROCK, Move.ROCK, Outcome.DRAW),
        (Move.ROCK, Move.SCISSORS, Outcome.PLAYER_WIN),
        (Move.ROCK, Move.PAPER, Outcome.COMPUTER_WIN),
        (Move.PAPER, Move.ROCK, Outcome.PLAYER_WIN),
        (Move.PAPER, Move.SCISSORS, Outcome.COMPUTER_WIN),
        (Move.SCISSORS, Move.PAPER, Outcome.PLAYER_WIN),
        (Move.SCISSORS, Move.ROCK, Outcome.COMPUTER_WIN),
    ],
)
def test_determine_outcome(player, computer, expected):
    assert determine_outcome(player, computer) == expected


def test_determine_outcome_rejects_invalid_moves():
    with pytest.raises(ValueError, match="valid Move"):
        determine_outcome("rock", Move.PAPER)


def test_create_round_result_records_moves_and_outcome():
    result = create_round_result(Move.ROCK, Move.SCISSORS)
    assert result == RoundResult(Move.ROCK, Move.SCISSORS, Outcome.PLAYER_WIN)


def test_calculate_score_includes_draws_in_win_rate_denominator():
    results = [
        create_round_result(Move.ROCK, Move.SCISSORS),
        create_round_result(Move.ROCK, Move.PAPER),
        create_round_result(Move.ROCK, Move.ROCK),
    ]
    assert calculate_score(results).wins == 1
    assert calculate_score(results).losses == 1
    assert calculate_score(results).draws == 1
    assert calculate_score(results).rounds_played == 3
    assert calculate_score(results).win_rate == pytest.approx(1 / 3)


def test_calculate_score_for_empty_history():
    assert calculate_score([]).win_rate == 0.0
    assert calculate_score([]).rounds_played == 0


def test_calculate_score_rejects_invalid_entries():
    with pytest.raises(ValueError, match="RoundResult"):
        calculate_score(["not a result"])


@pytest.mark.parametrize("best_of", [3, 5, 7])
def test_validate_best_of_accepts_supported_values(best_of):
    validate_best_of(best_of)


@pytest.mark.parametrize("best_of", [0, 1, 4, 9, True])
def test_validate_best_of_rejects_unsupported_values(best_of):
    with pytest.raises(ValueError, match="best_of"):
        validate_best_of(best_of)


def test_match_ends_when_player_reaches_majority():
    results = [
        create_round_result(Move.ROCK, Move.SCISSORS),
        create_round_result(Move.PAPER, Move.ROCK),
    ]
    assert match_outcome(results, 3) == Outcome.PLAYER_WIN


def test_match_does_not_count_draw_toward_target():
    results = [
        create_round_result(Move.ROCK, Move.ROCK),
        create_round_result(Move.PAPER, Move.ROCK),
    ]
    assert match_outcome(results, 3) is None


def test_match_outcome_rejects_invalid_best_of():
    with pytest.raises(ValueError):
        match_outcome([], 4)
