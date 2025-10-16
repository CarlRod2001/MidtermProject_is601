from decimal import Decimal, InvalidOperation
from app.exceptions import ValidationError, OperationError
from app.operations import OperationFactory
from app.calculation import Calculation


class Calculator:
    "Core calculator class handling operations, history, and state management."
    def __init__(self):
        self.history = []
        self.undone = []

    def validate_input(self, value):
        """Convert input to Decimal and validate."""
        try:
            return Decimal(value)
        except (InvalidOperation, ValueError):
            raise ValidationError(f"Invalid numeric input: {value}")

    def perform_calculation(self, a, b, operation_name):
        """Perform the calculation and store the result."""
        a = self.validate_input(a)
        b = self.validate_input(b)
        operation = OperationFactory.create(operation_name)

        result = operation.execute(a, b)
        calc = Calculation(a, b, operation_name, result)
        self.history.append(calc)
        self.undone.clear()
        return result

    def show_history(self):
        """Return a list of calculation strings."""
        return [str(calc) for calc in self.history]

    def undo(self):
        """Undo the last operation."""
        if not self.history:
            return False
        last = self.history.pop()
        self.undone.append(last)
        return True

    def redo(self):
        """Redo the last undone operation."""
        if not self.undone:
            return False
        calc = self.undone.pop()
        self.history.append(calc)
        return True

    def clear_history(self):
        """Clear all history and undo stacks."""
        self.history.clear()
        self.undone.clear()
