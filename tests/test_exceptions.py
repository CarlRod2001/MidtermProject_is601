import pytest
from app.exceptions import CalculatorError, ValidationError, OperationError, ConfigurationError

def test_inheritance():
    assert issubclass(ValidationError, CalculatorError)
    assert issubclass(OperationError, CalculatorError)
    assert issubclass(ConfigurationError, CalculatorError)

def test_exception_messages():
    e = ValidationError("Invalid input")
    assert "Invalid input" in str(e)
