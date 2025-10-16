import pytest
from decimal import Decimal
from app.operations import OperationFactory, OperationError

def test_add():
    op = OperationFactory.create("add")
    assert op.execute(Decimal("2"), Decimal("3")) == Decimal("5")

def test_subtract():
    op = OperationFactory.create("subtract")
    assert op.execute(Decimal("5"), Decimal("3")) == Decimal("2")

def test_divide_by_zero():
    op = OperationFactory.create("divide")
    with pytest.raises(OperationError):
        op.execute(Decimal("5"), Decimal("0"))

def test_root_of_zero_degree():
    op = OperationFactory.create("root")
    with pytest.raises(OperationError):
        op.execute(Decimal("8"), Decimal("0"))

def test_modulus_valid():
    op = OperationFactory.create("modulus")
    assert op.execute(Decimal("7"), Decimal("4")) == Decimal("3")

def test_percentage():
    op = OperationFactory.create("percent")
    assert op.execute(Decimal("1"), Decimal("2")) == Decimal("50")

def test_unknown_operation():
    with pytest.raises(OperationError):
        OperationFactory.create("fake")