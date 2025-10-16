from dataclasses import dataclass
from typing import List
import copy
from app.calculation import Calculation

@dataclass
class Memento:
    snapshot: List[dict]

class Caretaker:
    def __init__(self):
        self._undo_stack: List[Memento] = []
        self._redo_stack: List[Memento] = []

    def save(self, history_list):
        snap = [c.to_dict() for c in history_list]
        self._undo_stack.append(Memento(copy.deepcopy(snap)))
        self._redo_stack.clear()

    def undo(self, history):
        if not self._undo_stack:
            return False
        m = self._undo_stack.pop()
        # save current for redo
        current = [c.to_dict() for c in history.list()]
        self._redo_stack.append(Memento(current))
        # restore safely
        restored_items = []
        for d in m.snapshot:
            try:
                restored_items.append(Calculation.from_dict(d))
            except Exception:
                # fallback: skip invalid entries
                continue
        history._items = restored_items
        return True

    def redo(self, history):
        if not self._redo_stack:
            return False
        m = self._redo_stack.pop()
        current = [c.to_dict() for c in history.list()]
        self._undo_stack.append(Memento(current))
        restored_items = []
        for d in m.snapshot:
            try:
                restored_items.append(Calculation.from_dict(d))
            except Exception:
                continue
        history._items = restored_items
        return True