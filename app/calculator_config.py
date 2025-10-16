import os
from dotenv import load_dotenv

load_dotenv()

def _getenv(name, default, cast=str):
    v = os.getenv(name)
    if v is None:
        return cast(default)
    try:
        return cast(v)
    except Exception:
        return cast(default)

class Config:
    LOG_DIR = _getenv("CALCULATOR_LOG_DIR", "logs", str)
    HISTORY_DIR = _getenv("CALCULATOR_HISTORY_DIR", "history", str)
    HISTORY_FILE = _getenv("CALCULATOR_HISTORY_FILE", "history.csv", str)
    LOG_FILE = _getenv("CALCULATOR_LOG_FILE", "calculator.log", str)
    MAX_HISTORY_SIZE = _getenv("CALCULATOR_MAX_HISTORY_SIZE", 100, int)
    AUTO_SAVE = _getenv("CALCULATOR_AUTO_SAVE", "true", lambda s: str(s).lower() == "true")
    PRECISION = _getenv("CALCULATOR_PRECISION", 6, int)
    MAX_INPUT_VALUE = _getenv("CALCULATOR_MAX_INPUT_VALUE", 1e12, float)
    ENCODING = _getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8", str)