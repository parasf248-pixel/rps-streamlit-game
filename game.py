"""Rules and scoring for Rock, Paper, Scissors."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum


class Move(str, Enum):
    """The three moves available in Rock, Paper, Scissors."""

    ROCK = "Rock"
    PAPER = "Paper"
    SCISSORS = "Scissors"


class Outcome(str, Enum):
    """The result of a round or a completed match."""

    PLAYER_WIN = "Player wins"
    COMPUTER_WIN = "Computer wins"
    DRAW = "Draw"


@dataclass(frozen=True)
class RoundResult:
    """The two moves played and the resulting round outcome."""

    player_move: Move
    computer_move: Move
    outcome: Outcome


@dataclass(frozen=True)
class Score:
    """A summary of all rounds played in a match."""

    wins: int
    losses: int
    draws: int
    rounds_played: int
    win_rate: float


BEST_OF_OPTIONS = (3, 5, 7)
_WINNING_MOVES = {
    Move.ROCK: Move.PAPER,
    Move.PAPER: Move.SCISSORS,
    Move.SCISSORS: Move.ROCK,
}


def determine_outcome(player_move: Move, computer_move: Move) -> Outcome:
    """Return the outcome for two valid moves."""
    if not isinstance(player_move, Move) or not isinstance(computer_move, Move):
        raise ValueError("Both moves must be valid Move values.")
    if player_move == computer_move:
        return Outcome.DRAW
    if _WINNING_MOVES[player_move] == computer_move:
        return Outcome.COMPUTER_WIN
    return Outcome.PLAYER_WIN


def create_round_result(player_move: Move, computer_move: Move) -> RoundResult:
    """Create a round result using the game's rules."""
    return RoundResult(
        player_move=player_move,
        computer_move=computer_move,
        outcome=determine_outcome(player_move, computer_move),
    )


def calculate_score(results: Sequence[RoundResult]) -> Score:
    """Count round outcomes and calculate wins as a share of all rounds."""
    if any(not isinstance(result, RoundResult) for result in results):
        raise ValueError("Every result must be a RoundResult.")

    wins = sum(result.outcome == Outcome.PLAYER_WIN for result in results)
    losses = sum(result.outcome == Outcome.COMPUTER_WIN for result in results)
    draws = sum(result.outcome == Outcome.DRAW for result in results)
    rounds_played = len(results)
    win_rate = wins / rounds_played if rounds_played else 0.0
    return Score(wins, losses, draws, rounds_played, win_rate)


def validate_best_of(best_of: int) -> None:
    """Raise ValueError unless best_of is one of the supported match lengths."""
    if isinstance(best_of, bool) or best_of not in BEST_OF_OPTIONS:
        raise ValueError(f"best_of must be one of {BEST_OF_OPTIONS}.")


def match_outcome(results: Sequence[RoundResult], best_of: int) -> Outcome | None:
    """Return the match winner once they reach a majority, otherwise None."""
    validate_best_of(best_of)
    score = calculate_score(results)
    target = best_of // 2 + 1
    if score.wins >= target:
        return Outcome.PLAYER_WIN
    if score.losses >= target:
        return Outcome.COMPUTER_WIN
    return None
