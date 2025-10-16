from app.calculator import Calculator
from app.exceptions import ValidationError, OperationError


def calculator_repl():
    calc = Calculator()
    print("Calculator started. Type 'help' for commands.")

    valid_ops = [
        'add', 'subtract', 'multiply', 'divide',
        'power', 'root', 'modulus', 'int_divide',
        'percent', 'abs_diff'
    ]

    while True:
        try:
            cmd = input("\nEnter command: ").strip().lower()
            if not cmd:
                continue

            # ----- Help -----
            if cmd == 'help':
                print("Available Commands:")
                print("  " + ", ".join(valid_ops))
                print("  history - Show calculation history")
                print("  clear - Clear calculation history")
                print("  undo - Undo the last calculation")
                print("  redo - Redo the last undone calculation")
                print("  exit - Exit the calculator")
                continue

            # ----- Exit -----
            if cmd == 'exit':
                print("Goodbye!")
                break

            # ----- History -----
            if cmd == 'history':
                items = calc.show_history()
                if not items:
                    print("No history.")
                else:
                    for i, c in enumerate(items, 1):
                        print(f"{i}. {c}")
                continue

            # ----- Clear -----
            if cmd == 'clear':
                calc.clear_history()
                print("History cleared.")
                continue

            # ----- Undo -----
            if cmd == 'undo':
                ok = calc.undo()
                print("Undid last operation." if ok else "Nothing to undo.")
                continue

            # ----- Redo -----
            if cmd == 'redo':
                ok = calc.redo()
                print("Redid last operation." if ok else "Nothing to redo.")
                continue

            # ----- Arithmetic Operations -----
            if cmd in valid_ops:
                try:
                    a = input("First number: ").strip()
                    if a.lower() == 'cancel':
                        print("Cancelled.")
                        continue
                    b = input("Second number: ").strip()
                    if b.lower() == 'cancel':
                        print("Cancelled.")
                        continue

                    # FIX: correct argument order (a, b, operation)
                    result = calc.perform_calculation(a, b, cmd)
                    print(f"Result: {result}")

                except (ValidationError, OperationError) as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                continue

            print(f"Unknown command '{cmd}'. Type 'help'.")

        except KeyboardInterrupt:
            print("\nCancelled.")
            continue
        except EOFError:
            print("\nExit.")
            break