from decimal import Decimal
from app.exceptions import OperationError

class Operation:
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        raise NotImplementedError

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
        if b == Decimal('0'):
            raise OperationError("Division by zero")
        return a / b

class Power(Operation):
    def execute(self, a, b):
        # allow non-integer exponents by using float, then Decimal
        try:
            val = float(a) ** float(b)
            return Decimal(str(val))
        except Exception as e:
            raise OperationError(f"Power error: {e}")

class Root(Operation):
    def execute(self, a, b):
        # nth root: a ** (1/b)
        if b == Decimal('0'):
            raise OperationError("Root degree cannot be zero")
        try:
            # handle negative base with odd roots
            fa = float(a)
            fb = float(b)
            val = fa ** (1.0 / fb)
            return Decimal(str(val))
        except Exception as e:
            raise OperationError(f"Root error: {e}")

class Modulus(Operation):
    def execute(self, a, b):
        if b == Decimal('0'):
            raise OperationError("Modulus by zero")
        try:
            return a % b
        except Exception as e:
            # Decimal % Decimal should work, fallback
            try:
                return Decimal(str(float(a) % float(b)))
            except Exception:
                raise OperationError(f"Modulus error: {e}")

class IntegerDivision(Operation):
    def execute(self, a, b):
        if b == Decimal('0'):
            raise OperationError("Integer division by zero")
        return a // b

class Percentage(Operation):
    """(a / b) * 100"""
    def execute(self, a, b):
        if b == Decimal('0'):
            raise OperationError("Percentage denominator cannot be zero")
        return (a / b) * Decimal('100')

class AbsoluteDifference(Operation):
    def execute(self, a, b):
        return abs(a - b)

class OperationFactory:
    _ops = {
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

    @classmethod
    def create(cls, name: str):
        key = name.lower()
        op = cls._ops.get(key)
        if not op:
            raise OperationError(f"Unknown operation '{name}'")
        return op()