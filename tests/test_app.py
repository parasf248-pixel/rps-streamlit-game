"""Streamlit UI tests for match controls and session-state behavior."""

from pathlib import Path

from streamlit.testing.v1 import AppTest


def _run_app() -> AppTest:
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    return AppTest.from_file(str(app_path)).run(timeout=10)


def test_new_match_clears_history_and_preserves_settings():
    app = _run_app()
    app.selectbox(key="best_of").set_value(7).run(timeout=10)
    app.selectbox(key="difficulty").set_value("Smart").run(timeout=10)
    app.button(key="move_Rock").click().run(timeout=10)

    next(button for button in app.button if button.label == "New match").click().run(
        timeout=10
    )

    assert not app.exception
    assert app.session_state["round_results"] == []
    assert app.session_state["player_history"] == []
    assert app.session_state["best_of"] == 7
    assert app.session_state["difficulty"] == "Smart"


def test_reset_game_clears_history_and_restores_defaults():
    app = _run_app()
    app.selectbox(key="best_of").set_value(7).run(timeout=10)
    app.selectbox(key="difficulty").set_value("Smart").run(timeout=10)
    app.button(key="move_Rock").click().run(timeout=10)

    next(button for button in app.button if button.label == "Reset game").click().run(
        timeout=10
    )

    assert not app.exception
    assert app.session_state["round_results"] == []
    assert app.session_state["player_history"] == []
    assert app.session_state["best_of"] == 3
    assert app.session_state["difficulty"] == "Easy"


def test_invalid_session_data_is_reset_with_a_warning():
    app = _run_app()
    app.session_state["round_results"] = ["invalid result"]
    app.run(timeout=10)

    assert not app.exception
    assert app.session_state["round_results"] == []
    assert app.session_state["player_history"] == []
    assert any("invalid" in warning.value.lower() for warning in app.warning)
