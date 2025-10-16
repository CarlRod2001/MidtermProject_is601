import math
from app.exceptions import OperationError


class Operation:
    """Base class for all operations."""

    def execute(self, a, b):
        raise NotImplementedError("Subclasses must implement execute()")


class Add(Operation):
    def execute(self, a, b):
        return a + b


class Subtract(Operation):
    def execute(self, a, b):
        return a - b


class Multiply(Operation):
    def execute(self, a, b):
        return a * b


class Divide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Division by zero is not allowed.")
        return a / b


class Power(Operation):
    def execute(self, a, b):
        return a ** b


class Root(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot take zeroth root.")
        if a < 0 and b % 2 == 0:
            raise OperationError("Cannot take even root of a negative number.")
        return a ** (1 / b)


class Modulus(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Modulus by zero is not allowed.")
        return a % b


class IntegerDivision(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Integer division by zero is not allowed.")
        return a // b


class Percentage(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Percentage denominator cannot be zero.")
        return (a / b) * 100


class AbsoluteDifference(Operation):
    def execute(self, a, b):
        return abs(a - b)


class OperationFactory:
    """Factory to create operation instances based on command strings."""
    operations = {
        'add': Add,
        'subtract': Subtract,
        'multiply': Multiply,
        'divide': Divide,
        'power': Power,
        'root': Root,
        'modulus': Modulus,
        'int_divide': IntegerDivision,
        'percent': Percentage,
        'abs_diff': AbsoluteDifference
    }

    @staticmethod
    def create(name):
        op_class = OperationFactory.operations.get(name)
        if not op_class:
            raise OperationError(f"Unknown operation '{name}'")
        return op_class()