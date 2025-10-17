from app.calculator import Calculator
from app.exceptions import ValidationError, OperationError
from colorama import init, Fore, Back, Style

# Initialize Colorama
init(autoreset=True)

def calculator_repl():
    calc = Calculator()
    print(Back.WHITE + Fore.BLACK + "Calculator started. Type 'help' for commands.")

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
                print(Fore.YELLOW + "Available Commands:")
                print(Fore.CYAN + "  " + ", ".join(valid_ops))
                print(Fore.MAGENTA + "  history - Show calculation history")
                print(Fore.MAGENTA + "  clear - Clear calculation history")
                print(Fore.MAGENTA + "  undo - Undo the last calculation")
                print(Fore.MAGENTA + "  redo - Redo the last undone calculation")
                print(Fore.RED + "  exit - Exit the calculator")
                continue

            # ----- Exit -----
            if cmd == 'exit':
                print(Fore.YELLOW + "Goodbye!")
                break

            # ----- History -----
            if cmd == 'history':
                items = calc.show_history()
                if not items:
                    print(Fore.MAGENTA + "No history.")
                else:
                    for i, c in enumerate(items, 1):
                        print(Fore.MAGENTA + f"{i}. {c}")
                continue

            # ----- Clear -----
            if cmd == 'clear':
                calc.clear_history()
                print(Fore.CYAN + "History cleared.")
                continue

            # ----- Undo -----
            if cmd == 'undo':
                ok = calc.undo()
                print(Fore.MAGENTA + ("Undid last operation." if ok else "Nothing to undo."))
                continue

            # ----- Redo -----
            if cmd == 'redo':
                ok = calc.redo()
                print(Fore.MAGENTA + ("Redid last operation." if ok else "Nothing to redo."))
                continue

            # ----- Arithmetic Operations -----
            if cmd in valid_ops:
                try:
                    a = input("First number: ").strip()
                    if a.lower() == 'cancel':
                        print(Fore.RED + "Operation cancelled.")
                        continue
                    b = input("Second number: ").strip()
                    if b.lower() == 'cancel':
                        print(Fore.RED + "Operation cancelled.")
                        continue

                    # perform calculation
                    calc_obj = calc.perform_calculation(a, b, cmd)

                    # ✅ print ONLY numeric result
                    print(Fore.GREEN + f"Result: {calc_obj.result}")

                except (ValidationError, OperationError) as e:
                    print(Fore.RED + f"Error: {e}")
                except Exception as e:
                    print(Fore.RED + f"Unexpected error: {e}")
                continue

            print(Fore.YELLOW + f"Unknown command '{cmd}'. Type 'help'.")

        except KeyboardInterrupt:
            print(Fore.RED + "\nCancelled.")
            continue
        except EOFError:
            print(Fore.BLACK + "\nExit.")
            break