from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Calculation:
    "Represents a single calculation record with operands, operation, result, and timestamp."
    operation: str
    operand1: Decimal
    operand2: Decimal
    result: Decimal
    timestamp: datetime = datetime.now()

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "operation": self.operation,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "result": str(self.result),
        }

    @classmethod
    def from_dict(cls, d):
        from decimal import Decimal
        from datetime import datetime
        ts = datetime.fromisoformat(d["timestamp"]) if "timestamp" in d else datetime.now()
        
        return cls(
            operation=d["operation"],
            operand1=Decimal(d["operand1"]),
            operand2=Decimal(d["operand2"]),
            result=Decimal(d["result"]),
            timestamp=ts
        )

    def __str__(self):
        t = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{t}] {self.operation}({self.operand1}, {self.operand2}) = {self.result}"
