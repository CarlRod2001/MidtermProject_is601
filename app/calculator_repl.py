from decimal import Decimal
import logging
from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.operations import OperationFactory


def calculator_repl():
    """
    Read-Eval-Print Loop (REPL) for the calculator application.
    Provides an interactive command-line interface for users to perform calculations.
    """

    try:
        calc = Calculator()
        print("Calculator started. Type 'help' for commands.")

        while True:
            try:
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    print("\nAvailable commands:")
                    print("  add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff")
                    print("  history - Show calculation history")
                    print("  clear - Clear calculation history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last undone calculation")
                    print("  exit - Exit the calculator")
                    continue

                if command == 'exit':
                    print("Goodbye!")
                    break

                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print("No calculations in history")
                    else:
                        print("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    calc.history.clear()
                    print("History cleared")
                    continue

                if command == 'undo':
                    if calc.undo():
                        print("Operation undone")
                    else:
                        print("Nothing to undo")
                    continue

                if command == 'redo':
                    if calc.redo():
                        print("Operation redone")
                    else:
                        print("Nothing to redo")
                    continue

                # Perform arithmetic operations
                if command in [
                    'add', 'subtract', 'multiply', 'divide',
                    'power', 'root', 'modulus', 'int_divide',
                    'percent', 'abs_diff'
                ]:
                    try:
                        print("\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print("Operation cancelled")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print("Operation cancelled")
                            continue

                        # Create operation and perform it
                        operation = OperationFactory.create(command)
                        result = calc.perform_calculation(a, b, command)

                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(f"\nResult: {result}")

                    except (ValidationError, OperationError) as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                    continue

                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nOperation cancelled")
                continue
            except EOFError:
                print("\nInput terminated. Exiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

    except Exception as e:
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise