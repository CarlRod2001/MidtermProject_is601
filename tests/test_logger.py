import os
import logging
from importlib import reload
from app.calculator_config import Config

from app import logger as logmod
    
def test_logger_file_created(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "LOG_DIR", str(tmp_path))
    monkeypatch.setattr(Config, "LOG_FILE", "calc.log")

    logger_instance = logging.getLogger("calculator")
    
    for handler in logger_instance.handlers[:]:
        logger_instance.removeHandler(handler)
        
    reload(logmod)

    path = tmp_path / "calc.log"

    logmod.logger.info("Test entry in temp directory")
    
    for handler in logmod.logger.handlers:
        handler.flush()

    assert path.exists(), f"Expected log file at {path}, but none found."
    
    content = path.read_text(encoding=Config.ENCODING)
    assert "Test entry in temp directory" in content

    for handler in logger_instance.handlers[:]:
        logger_instance.removeHandler(handler)