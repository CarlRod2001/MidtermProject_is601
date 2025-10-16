import pytest
from decimal import Decimal
from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from unittest.mock import patch

def test_valid_addition():
    calc = Calculator()
    result = calc.perform_calculation("1", "2", "add")
    assert result.result == Decimal("3")

def test_invalid_number():
    calc = Calculator()
    with pytest.raises(ValidationError):
        calc.perform_calculation("a", "2", "add")

def test_unknown_operation():
    calc = Calculator()
    with pytest.raises(OperationError):
        calc.perform_calculation("1", "2", "unknown")

def test_operation_error(monkeypatch):
    from app.operations import Add
    # Must include `self` as first argument for instance method
    def bad_execute(self, a, b):
        raise OperationError("test error")

    monkeypatch.setattr(Add, "execute", bad_execute)
    calc = Calculator()
    with pytest.raises(OperationError):
        calc.perform_calculation("1", "2", "add")

def test_undo_redo_behavior():
    calc = Calculator()
    calc.perform_calculation("1", "2", "add")
    prev = calc.history.list().copy()
    calc.undo()
    calc.redo()
    assert calc.history.list() == prev

def test_undo_logs_nothing(monkeypatch):
    calc = Calculator()
    # force caretaker.undo to return False
    monkeypatch.setattr(calc._caretaker, "undo", lambda hist: False)
    with patch("app.logger.logger.info") as mock_logger:
        result = calc.undo()
        assert result is False
        mock_logger.assert_called_with("Nothing to undo")

def test_redo_logs_nothing(monkeypatch):
    calc = Calculator()
    # force caretaker.redo to return False
    monkeypatch.setattr(calc._caretaker, "redo", lambda hist: False)
    with patch("app.logger.logger.info") as mock_logger:
        result = calc.redo()
        assert result is False
        mock_logger.assert_called_with("Nothing to redo")

def test_clear_history_logs(monkeypatch):
    calc = Calculator()
    calc.perform_calculation("1", "2", "add")
    with patch("app.logger.logger.info") as mock_logger:
        calc.clear_history()
        assert calc.show_history() == []
        mock_logger.assert_called_with("Cleared history")