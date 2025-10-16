import pytest
from decimal import Decimal
from app.operations import OperationFactory, OperationError, Operation

def test_base_operation_not_implemented():
    op = Operation()
    with pytest.raises(NotImplementedError):
        op.execute(Decimal('1'), Decimal('1'))

def test_add():
    op = OperationFactory.create("add")
    assert op.execute(Decimal("2"), Decimal("3")) == Decimal("5")

def test_subtract():
    op = OperationFactory.create("subtract")
    assert op.execute(Decimal("5"), Decimal("3")) == Decimal("2")
    assert op.execute(Decimal("3"), Decimal("5")) == Decimal("-2")

def test_multiply():
    op = OperationFactory.create("multiply")
    assert op.execute(Decimal("4"), Decimal("5")) == Decimal("20")
    assert op.execute(Decimal("-2"), Decimal("3")) == Decimal("-6")

def test_divide_valid():
    op = OperationFactory.create("divide")
    assert op.execute(Decimal("10"), Decimal("5")) == Decimal("2")

def test_divide_by_zero():
    op = OperationFactory.create("divide")
    with pytest.raises(OperationError, match="Division by zero"):
        op.execute(Decimal("5"), Decimal("0"))

def test_integer_division_valid():
    op = OperationFactory.create("int_divide")
    assert op.execute(Decimal("10"), Decimal("3")) == Decimal("3")

def test_integer_division_by_zero():
    op = OperationFactory.create("int_divide")
    with pytest.raises(OperationError, match="Integer division by zero"):
        op.execute(Decimal("5"), Decimal("0"))

def test_power_valid():
    op = OperationFactory.create("power")
    assert op.execute(Decimal("2"), Decimal("3")) == Decimal("8.0")
    assert op.execute(Decimal("9"), Decimal("0.5")) == Decimal("3.0")

def test_power_error_path():
    op = OperationFactory.create("power")
    with pytest.raises(OperationError, match="Power error"):
        op.execute(Decimal("-4"), Decimal("0.5"))

def test_root_valid():
    op = OperationFactory.create("root")
    assert op.execute(Decimal("8"), Decimal("3")) == pytest.approx(Decimal("2.0"))
    assert op.execute(Decimal("16"), Decimal("2")) == Decimal("4.0")

def test_root_of_zero_degree():
    op = OperationFactory.create("root")
    with pytest.raises(OperationError, match="Root degree cannot be zero"):
        op.execute(Decimal("8"), Decimal("0"))

def test_root_error_path():
    op = OperationFactory.create("root")
    with pytest.raises(OperationError, match="Root error"):
        op.execute(Decimal("-4"), Decimal("2"))

def test_modulus_valid():
    op = OperationFactory.create("modulus")
    assert op.execute(Decimal("7"), Decimal("4")) == Decimal("3")

def test_modulus_by_zero():
    op = OperationFactory.create("modulus")
    with pytest.raises(OperationError, match="Modulus by zero"):
        op.execute(Decimal("7"), Decimal("0"))

def test_modulus_fallback_path():
    op = OperationFactory.create("modulus")
    a = Decimal('5.5')
    b = Decimal('2.0')
    assert op.execute(a, b) == Decimal('1.5')

def test_percentage_valid():
    op = OperationFactory.create("percent")
    assert op.execute(Decimal("1"), Decimal("2")) == Decimal("50")

def test_percentage_denominator_zero():
    op = OperationFactory.create("percent")
    with pytest.raises(OperationError, match="Percentage denominator cannot be zero"):
        op.execute(Decimal("10"), Decimal("0"))

def test_absolute_difference():
    op = OperationFactory.create("abs_diff")
    assert op.execute(Decimal("10"), Decimal("4")) == Decimal("6")
    assert op.execute(Decimal("4"), Decimal("10")) == Decimal("6")

def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation 'fake'"):
        OperationFactory.create("fake")
