from decimal import Decimal
from app.calculation import Calculation

def test_to_and_from_dict():
    # Correct argument order
    c = Calculation(Decimal("1"), Decimal("2"), "add", Decimal("3"))
    d = c.to_dict()
    restored = Calculation.from_dict(d)

    assert restored.operation == "add"
    assert restored.operand1 == Decimal("1")
    assert restored.operand2 == Decimal("2")
    assert restored.result == Decimal("3")

def test_str_representation():
    c = Calculation(Decimal("1"), Decimal("2"), "add", Decimal("3"))
    s = str(c)
    assert "add" in s
    assert "(" in s
    assert "=" in s
