def test_import_logger_consistency():
    import app.input_validators as iv
    assert iv.logger.name == "calculator"
    assert iv.logger.hasHandlers()
