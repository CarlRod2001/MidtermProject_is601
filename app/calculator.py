from decimal import Decimal, InvalidOperation
from app.operations import OperationFactory
from app.exceptions import OperationError, ValidationError
from app.calculation import Calculation
from app.calculator_memento import Caretaker
from app.history import History
from app.logger import logger


class Calculator:
    """Core Calculator handling calculations, history, and undo/redo with memento."""
    def __init__(self):
        self.history = History()
        self._caretaker = Caretaker()
        self._observers = []

    # ----- Observer Pattern -----
    def add_observer(self, observer):
        self._observers.append(observer)

    def _notify_observers(self, calculation):
        for observer in self._observers:
            try:
                observer.update(calculation)
            except Exception as e:  # pragma: no cover
                logger.error(f"Observer error: {e}")

    # ----- Validation -----
    def _validate_number(self, value):
        try:
            return Decimal(value)
        except (InvalidOperation, TypeError):
            raise ValidationError(f"Invalid numeric input: {value}")

    # ----- Core Calculation -----
    def perform_calculation(self, a, b, operation_name):
        """Perform a calculation, save to history, notify observers, and store memento."""
        num1 = self._validate_number(a)
        num2 = self._validate_number(b)
        operation = OperationFactory.create(operation_name)

        result = operation.execute(num1, num2)
        calc = Calculation(num1, num2, operation_name, result)

        # Add calculation to history and save snapshot
        self.history.push(calc)
        self._caretaker.save(self.history.list())

        self._notify_observers(calc)
        logger.info(f"Performed {operation_name}({num1}, {num2}) = {result}")
        return result

    # ----- Undo / Redo -----
    def undo(self):
        """Undo last operation using caretaker."""
        if self._caretaker.undo(self.history):
            logger.info("Undo last operation")
            return True
        logger.info("Nothing to undo")
        return False

    def redo(self):
        """Redo last undone operation using caretaker."""
        if self._caretaker.redo(self.history):
            logger.info("Redo operation")
            return True
        logger.info("Nothing to redo")
        return False

    # ----- History Management -----
    def show_history(self):
        """Return list of calculation history."""
        return self.history.list()

    def clear_history(self):
        """Clear history and caretaker stacks."""
        self.history.clear()
        self._caretaker = Caretaker()
        logger.info("Cleared history")