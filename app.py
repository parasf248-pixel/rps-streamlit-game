"""Streamlit interface for Rock, Paper, Scissors."""

from __future__ import annotations

from typing import Any

import streamlit as st

from ai import Difficulty, choose_computer_move
from game import (
    BEST_OF_OPTIONS,
    Move,
    Outcome,
    RoundResult,
    calculate_score,
    create_round_result,
    determine_outcome,
    match_outcome,
    validate_best_of,
)

_EMOJI = {Move.ROCK: "🪨", Move.PAPER: "📄", Move.SCISSORS: "✂️"}
_STATE_DEFAULTS: dict[str, Any] = {
    "round_results": [],
    "player_history": [],
    "best_of": 3,
    "difficulty": Difficulty.EASY.value,
}


def _reset_match(*, reset_settings: bool = False) -> None:
    st.session_state.round_results = []
    st.session_state.player_history = []
    if reset_settings:
        st.session_state.best_of = 3
        st.session_state.difficulty = Difficulty.EASY.value


def _reset_game() -> None:
    _reset_match(reset_settings=True)
    st.session_state.state_warning = False


def _valid_session_state() -> bool:
    results = st.session_state.get("round_results")
    history = st.session_state.get("player_history")
    best_of = st.session_state.get("best_of")
    difficulty = st.session_state.get("difficulty")
    return (
        isinstance(results, list)
        and all(isinstance(result, RoundResult) for result in results)
        and all(
            isinstance(result.player_move, Move)
            and isinstance(result.computer_move, Move)
            and isinstance(result.outcome, Outcome)
            and result.outcome
            == determine_outcome(result.player_move, result.computer_move)
            for result in results
        )
        and isinstance(history, list)
        and all(isinstance(move, Move) for move in history)
        and len(results) == len(history)
        and isinstance(best_of, int)
        and not isinstance(best_of, bool)
        and best_of in BEST_OF_OPTIONS
        and difficulty in {item.value for item in Difficulty}
        and all(
            result.player_move == move
            for result, move in zip(results, history, strict=True)
        )
    )


def _initialize_session() -> None:
    missing_key = any(key not in st.session_state for key in _STATE_DEFAULTS)
    if missing_key:
        for key, value in _STATE_DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = (
                    value.copy() if isinstance(value, list) else value
                )
    if not _valid_session_state():
        _reset_match(reset_settings=True)
        st.session_state.state_warning = True


def _play_round(player_move: Move) -> None:
    results: list[RoundResult] = st.session_state.round_results
    history: list[Move] = st.session_state.player_history
    best_of = st.session_state.best_of
    if match_outcome(results, best_of) is not None:
        return

    difficulty = Difficulty(st.session_state.difficulty)
    computer_move = choose_computer_move(difficulty, history)
    result = create_round_result(player_move, computer_move)
    st.session_state.round_results = [*results, result]
    st.session_state.player_history = [*history, player_move]


def _describe_round_result(result: RoundResult) -> str:
    if result.outcome == Outcome.DRAW:
        return "It's a draw!"
    if result.outcome == Outcome.PLAYER_WIN:
        return "You win this round!"
    return "The computer wins this round."


def _show_round_history(results: list[RoundResult]) -> None:
    if not results:
        st.info("Your round history will appear here after your first move.")
        return

    rows = [
        {
            "Round": number,
            "Your move": f"{_EMOJI[result.player_move]} {result.player_move.value}",
            "Computer": (
                f"{_EMOJI[result.computer_move]} {result.computer_move.value}"
            ),
            "Result": result.outcome.value,
        }
        for number, result in enumerate(results, start=1)
    ]
    st.dataframe(rows, hide_index=True, use_container_width=True)


def main() -> None:
    st.set_page_config(
        page_title="Rock, Paper, Scissors",
        page_icon="✊",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
        .stApp { background: linear-gradient(160deg, #f3fbf7 0%, #f8f6ff 100%); }
        .block-container { max-width: 860px; padding-top: 2rem; }
        [data-testid="stButton"] button {
            min-height: 3.5rem;
            border-radius: 0.8rem;
            font-weight: 650;
        }
        @media (max-width: 640px) {
            .block-container { padding: 1rem 0.8rem 2rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    _initialize_session()

    with st.sidebar:
        st.title("How to play")
        st.markdown(
            """
            Choose **Rock**, **Paper**, or **Scissors** each round.

            - Rock beats Scissors.
            - Scissors beats Paper.
            - Paper beats Rock.
            - A draw does not count toward either player's target.
            - First to a majority wins the match.
            """
        )
        st.divider()
        selected_best_of = st.selectbox(
            "Match length",
            BEST_OF_OPTIONS,
            format_func=lambda value: f"Best of {value}",
            key="best_of",
            disabled=bool(st.session_state.round_results),
        )
        st.selectbox(
            "Computer difficulty",
            [difficulty.value for difficulty in Difficulty],
            key="difficulty",
            disabled=bool(st.session_state.round_results),
        )
        st.button(
            "New match",
            use_container_width=True,
            on_click=_reset_match,
        )
        st.button(
            "Reset game",
            use_container_width=True,
            on_click=_reset_game,
        )

    if st.session_state.pop("state_warning", False):
        st.warning("Game data was invalid, so the game has been reset.")

    st.title("✊ Rock, Paper, Scissors")
    st.caption("A quick, friendly match against the computer.")

    results: list[RoundResult] = st.session_state.round_results
    best_of = selected_best_of
    validate_best_of(best_of)
    score = calculate_score(results)
    winner = match_outcome(results, best_of)
    target = best_of // 2 + 1

    metrics = st.columns(4)
    metrics[0].metric("Your wins", score.wins)
    metrics[1].metric("Computer wins", score.losses)
    metrics[2].metric("Draws", score.draws)
    metrics[3].metric("Win rate", f"{score.win_rate:.0%}")
    st.progress(min(score.wins, target) / target, text=f"Your target: {target} wins")

    if winner is None:
        st.subheader(f"Round {score.rounds_played + 1}")
        st.write("Make your move:")
        move_columns = st.columns(3)
        for column, move in zip(move_columns, Move, strict=True):
            with column:
                if st.button(
                    f"{_EMOJI[move]}  {move.value}",
                    key=f"move_{move.value}",
                    use_container_width=True,
                ):
                    _play_round(move)
                    st.rerun()
    elif winner == Outcome.PLAYER_WIN:
        st.success(f"You won the match! First to {target} wins — nicely played!")
    else:
        st.info("The computer won this match. Ready for a rematch?")

    if results:
        latest = results[-1]
        st.markdown(
            f"**Last round:** You played {_EMOJI[latest.player_move]} "
            f"**{latest.player_move.value}**; the computer played "
            f"{_EMOJI[latest.computer_move]} **{latest.computer_move.value}**. "
            f"{_describe_round_result(latest)}"
        )

    st.subheader("Round-by-round history")
    _show_round_history(results)

    with st.expander("How the AI thinks"):
        st.markdown(
            """
            - **Easy** picks a move at random.
            - **Medium** usually picks the move that beats your last move, but
              sometimes chooses randomly instead.
            - **Smart** looks at which moves you use most and what you tend to
              play after your previous move. It predicts your next move from
              those patterns, then picks the move that beats that prediction.
            - If there is not enough history to spot a pattern, Smart uses your
              overall move counts; with no history, it starts randomly.

            The computer can only use moves from this match, so starting a new
            match gives it a fresh start.
            """
        )


if __name__ == "__main__":
    main()
