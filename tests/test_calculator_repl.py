from unittest.mock import patch, MagicMock
import re
import pytest
from app.calculator_repl import calculator_repl
from app.exceptions import ValidationError, OperationError


def test_exit_immediately():
    with patch("builtins.input", side_effect=["exit"]):
        calculator_repl()


def test_help(capsys):
    with patch("builtins.input", side_effect=["help", "exit"]):
        calculator_repl()
    out = capsys.readouterr().out
    assert "Available Commands" in out
    assert "history - Show calculation history" in out


def test_history_empty(capsys):
    fake_calc = MagicMock()
    fake_calc.show_history.return_value = []
    with patch("app.calculator_repl.Calculator", return_value=fake_calc):
        with patch("builtins.input", side_effect=["history", "exit"]):
            calculator_repl()
    out = capsys.readouterr().out
    assert "No history" in out


def test_history_with_items(capsys):
    fake_calc = MagicMock()
    fake_calc.show_history.return_value = ["add(1, 2) = 3"]
    with patch("app.calculator_repl.Calculator", return_value=fake_calc):
        with patch("builtins.input", side_effect=["history", "exit"]):
            calculator_repl()
    out = capsys.readouterr().out
    assert "add(1, 2)" in out


def test_clear(capsys):
    fake_calc = MagicMock()
    with patch("app.calculator_repl.Calculator", return_value=fake_calc):
        with patch("builtins.input", side_effect=["clear", "exit"]):
            calculator_repl()
    out = capsys.readouterr().out
    assert "History cleared" in out


def test_undo_redo(capsys):
    fake_calc = MagicMock()
    fake_calc.undo.return_value = True
    fake_calc.redo.return_value = False
    with patch("app.calculator_repl.Calculator", return_value=fake_calc):
        with patch("builtins.input", side_effect=["undo", "redo", "exit"]):
            calculator_repl()
    out = capsys.readouterr().out
    assert "Undid last operation" in out
    assert "Nothing to redo" in out


def test_valid_operation(capsys):
    fake_calc = MagicMock()
    result_mock = MagicMock(result=42)
    fake_calc.perform_calculation.return_value = result_mock
    with patch("app.calculator_repl.Calculator", return_value=fake_calc):
        with patch("builtins.input", side_effect=["add", "2", "40", "exit"]):
            calculator_repl()
    out = capsys.readouterr().out
    assert "Result: 42" in out


def test_cancel_input(capsys):
    fake_calc = MagicMock()
    with patch("app.calculator_repl.Calculator", return_value=fake_calc):
        with patch("builtins.input", side_effect=["add", "cancel", "exit"]):
            calculator_repl()
        with patch("builtins.input", side_effect=["add", "1", "cancel", "exit"]):
            calculator_repl()

    out = capsys.readouterr().out

    # Remove ANSI color codes for easier assertion
    clean_out = re.sub(r"\x1b\[[0-9;]*m", "", out)
    assert "Operation cancelled." in clean_out

def test_exceptions(capsys):
    fake_calc = MagicMock()

    # ValidationError
    fake_calc.perform_calculation.side_effect = ValidationError("Bad input")
    with patch("app.calculator_repl.Calculator", return_value=fake_calc):
        with patch("builtins.input", side_effect=["add", "1", "2", "exit"]):
            calculator_repl()
    out = capsys.readouterr().out
    assert "Error: Bad input" in out

    # OperationError
    fake_calc.perform_calculation.side_effect = OperationError("Bad op")
    with patch("app.calculator_repl.Calculator", return_value=fake_calc):
        with patch("builtins.input", side_effect=["add", "1", "2", "exit"]):
            calculator_repl()
    out = capsys.readouterr().out
    assert "Error: Bad op" in out

    # Generic Exception
    fake_calc.perform_calculation.side_effect = Exception("Unexpected")
    with patch("app.calculator_repl.Calculator", return_value=fake_calc):
        with patch("builtins.input", side_effect=["add", "1", "2", "exit"]):
            calculator_repl()
    out = capsys.readouterr().out
    assert "Unexpected error" in out


def test_keyboard_interrupt(capsys):
    with patch("builtins.input", side_effect=[KeyboardInterrupt, "exit"]):
        calculator_repl()
    out = capsys.readouterr().out
    assert "Cancelled" in out or "Goodbye" in out


def test_eof_exit(capsys):
    with patch("builtins.input", side_effect=[EOFError]):
        calculator_repl()
    out = capsys.readouterr().out
    assert "Exit" in out


def test_unknown_command(capsys):
    fake_calc = MagicMock()
    with patch("app.calculator_repl.Calculator", return_value=fake_calc):
        with patch("builtins.input", side_effect=["foobar", "exit"]):
            calculator_repl()
    out = capsys.readouterr().out
    assert "Unknown command" in out
