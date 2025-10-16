import os
from typing import List
import pandas as pd
from app.calculation import Calculation
from app.calculator_config import Config
from .logger import logger

os.makedirs(Config.HISTORY_DIR, exist_ok=True)
_HISTORY_PATH = os.path.join(Config.HISTORY_DIR, Config.HISTORY_FILE)

class Observer:
    def notify(self, calc: Calculation):
        raise NotImplementedError

class LoggingObserver(Observer):
    def notify(self, calc: Calculation):
        try:
            logger.info(f"{calc.operation} {calc.operand1} {calc.operand2} = {calc.result}")
        except Exception:
            logger.exception("LoggingObserver error")

class AutoSaveObserver(Observer):
    def __init__(self, history):
        self.history = history

    def notify(self, calc: Calculation):
        if Config.AUTO_SAVE:
            try:
                self.history.save(_HISTORY_PATH)
            except Exception:
                logger.exception("AutoSaveObserver error")

class History:
    def __init__(self):
        self._items: List[Calculation] = []

    def push(self, calc: Calculation):
        self._items.append(calc)
        # keep bounded size
        if len(self._items) > Config.MAX_HISTORY_SIZE:
            self._items = self._items[-Config.MAX_HISTORY_SIZE:]

    def pop(self):
        return self._items.pop()

    def clear(self):
        self._items.clear()

    def list(self) -> List[Calculation]:
        return list(self._items)

    def to_dataframe(self):
        rows = [c.to_dict() for c in self._items]
        if not rows:
            # empty df with columns
            return pd.DataFrame(columns=["timestamp","operation","operand1","operand2","result"])
        return pd.DataFrame(rows)

    def save(self, path: str = None):
        path = path or _HISTORY_PATH
        df = self.to_dataframe()
        df.to_csv(path, index=False, encoding=Config.ENCODING)

    def load(self, path: str = None):
        path = path or _HISTORY_PATH
        if not os.path.exists(path):
            return
        try:
            df = pd.read_csv(path, dtype=str)
            self._items = [Calculation.from_dict({
                "timestamp": row.get("timestamp"),
                "operation": row["operation"],
                "operand1": row["operand1"],
                "operand2": row["operand2"],
                "result": row["result"]
            }) for _, row in df.iterrows()]
        except Exception as e:
            logger.exception(f"Error loading history: {e}")
            raise