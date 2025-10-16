from datetime import datetime


class Calculation:
    "Represents a single calculation record with operands, operation, result, and timestamp."
    
    def __init__(self, a, b, operation, result):
        self.a = a
        self.b = b
        self.operation = operation
        self.result = result
        self.timestamp = datetime.now()

    def __str__(self):
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.a} {self.operation} {self.b} = {self.result}"