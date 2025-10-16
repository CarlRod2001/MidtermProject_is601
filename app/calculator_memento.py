from dataclasses import dataclass
from typing import List
import copy
from app.calculation import Calculation
from app.history import History

@dataclass
class CalculatorMemento:
    """Stores a snapshot of calculator history."""
    history: List[Calculation]

class Caretaker:
    """
    Manages undo and redo stacks using the Memento pattern.
    """
    def __init__(self):
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []

    def save(self, history_list: List[Calculation]):
        """
        Save a snapshot of the current history.
        Should be called BEFORE a new calculation is added.
        """
        snap = copy.deepcopy(history_list)
        self._undo_stack.append(CalculatorMemento(snap))
        self._redo_stack.clear()  # clear redo when new operation occurs

    def undo(self, history: History) -> bool:
        """Undo the last operation."""
        if not self._undo_stack:
            return False

        # Save current state to redo stack
        self._redo_stack.append(CalculatorMemento(copy.deepcopy(history.list())))

        # Restore previous state from undo stack
        memento_to_restore = self._undo_stack.pop()
        history.set_items(copy.deepcopy(memento_to_restore.history))
        return True

    def redo(self, history: History) -> bool:
        """Redo the last undone operation."""
        if not self._redo_stack:
            return False

        # Save current state to undo stack
        self._undo_stack.append(CalculatorMemento(copy.deepcopy(history.list())))

        # Restore history from redo stack
        memento_to_restore = self._redo_stack.pop()
        history.set_items(copy.deepcopy(memento_to_restore.history))
        return True