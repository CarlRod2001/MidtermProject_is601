class CalculatorError(Exception):
    """
    Base exception class for calculator-specific errors.
    All custom exceptions for the calculator application should inherit from this class.
    """
    pass


class ValidationError(CalculatorError):
    """
    Raised when input validation fails.
    This exception is triggered when user inputs are invalid, such as non-numeric values
    or unsupported operations.
    """
    pass


class OperationError(CalculatorError):
    """
    Raised when a calculation operation fails.
    This exception is triggered during arithmetic operations, such as division by zero
    or invalid mathematical operations.
    """
    pass


class ConfigurationError(CalculatorError):
    """
    Raised when calculator configuration is invalid.
    This exception is triggered when there are issues with the calculator's settings
    """
    pass