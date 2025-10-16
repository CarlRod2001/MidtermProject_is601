from app.calculator_memento import Caretaker
from app.history import History
from app.calculation import Calculation
from decimal import Decimal

def test_undo_redo_flow():
    h = History()
    c1 = Calculation("add", Decimal("1"), Decimal("2"), Decimal("3"))
    c2 = Calculation("subtract", Decimal("4"), Decimal("1"), Decimal("3"))
    ct = Caretaker()

    h.push(c1)
    ct.save(h.list())
    h.push(c2)

    assert len(h.list()) == 2
    assert ct.undo(h)
    assert len(h.list()) == 1
    assert ct.redo(h)
    assert len(h.list()) == 2