from app.calculator_config import Config

def test_default_config_values():
    assert isinstance(Config.LOG_DIR, str)
    assert isinstance(Config.AUTO_SAVE, bool)
    assert Config.PRECISION > 0