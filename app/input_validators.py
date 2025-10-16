import logging
import os
from app.calculator_config import Config

os.makedirs(Config.LOG_DIR, exist_ok=True)
_LOG_PATH = os.path.join(Config.LOG_DIR, Config.LOG_FILE)

logger = logging.getLogger("calculator")
logger.setLevel(logging.INFO)

if not logger.handlers:
    fh = logging.FileHandler(_LOG_PATH, encoding=Config.ENCODING)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)