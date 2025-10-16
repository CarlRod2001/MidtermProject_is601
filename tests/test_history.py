from decimal import Decimal
from datetime import datetime
from app.history import History, LoggingObserver, AutoSaveObserver
from app.calculation import Calculation
import logging

class DummyCalc:
    def __init__(self):
        self.config = type("C", (), {"AUTO_SAVE": True})()
        self.saved = False
    def save_history(self):
        self.saved = True

def test_push_and_list():
    h = History()
    c = Calculation("add", Decimal("1"), Decimal("2"), Decimal("3"))
    h.push(c)
    assert len(h.list()) == 1

def test_logging_observer_logs(caplog):
    obs = LoggingObserver()
    c = Calculation("add", Decimal("1"), Decimal("2"), Decimal("3"))
    with caplog.at_level(logging.INFO):
        obs.update(c)
    assert "Calculation performed" in caplog.text

def test_autosave_observer_triggers_save():
    calc = DummyCalc()
    obs = AutoSaveObserver(calc)
    c = Calculation("add", Decimal("1"), Decimal("2"), Decimal("3"))
    obs.update(c)
    assert calc.saved