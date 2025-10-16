from unittest.mock import patch, MagicMock
from app.calculator_repl import calculator_repl

def test_exit_immediately(monkeypatch):
    mock_input = MagicMock(side_effect=["exit"])
    with patch("builtins.input", mock_input):
        calculator_repl()
    assert mock_input.called
