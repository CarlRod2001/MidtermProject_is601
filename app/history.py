import logging
import os
from abc import ABC, abstractmethod
from typing import Any, List
from app.calculation import Calculation
from app.calculator_config import Config 

class HistoryObserver(ABC):
    """Abstract base class for calculator observers."""
    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        pass # pragma: no cover


# --- Concrete Observers (Professor's Version) ---

class LoggingObserver(HistoryObserver):
    """Observer that logs calculations."""
    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        logging.info(
            f"Calculation performed: {calculation.operation} "
            f"({calculation.operand1}, {calculation.operand2}) = "
            f"{calculation.result}"
        )


class AutoSaveObserver(HistoryObserver):
    """Observer that automatically saves calculations."""
    def __init__(self, calculator: Any):
        """
        Args: calculator (Any): Must have 'config' and 'save_history' attributes.
        """
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        """Trigger auto-save if enabled."""
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        if self.calculator.config.AUTO_SAVE: # Adjusted to use YOUR Config casing
            self.calculator.save_history()
            logging.info("History auto-saved")


# --- Core History Class ---

class History:
    """Manages the ordered list of Calculation objects."""
    def __init__(self):
        self._items: List[Calculation] = []

    def push(self, calc: Calculation):
        """Adds a new calculation to the end of the history."""
        self._items.append(calc)
        # Apply MAX_HISTORY_SIZE limit (if configured)
        if hasattr(Config, 'MAX_HISTORY_SIZE') and len(self._items) > Config.MAX_HISTORY_SIZE:
             self._items = self._items[-Config.MAX_HISTORY_SIZE:]

    def pop(self):
        """Removes and returns the last calculation."""
        return self._items.pop()

    def clear(self):
        """Clears all history items."""
        self._items.clear()

    def list(self) -> List[Calculation]:
        """Returns a copy of the current history list."""
        return list(self._items)

    def set_items(self, new_items: List[Calculation]):
        """Replace history safely (used for undo/redo)."""
        # Assign the list directly (assuming new_items is already a copy from Memento)
        self._items = new_items 
