from lexer_analyzer import Lexer
from parser import Parser
from interpreter import Interpreter
from colorama import Fore, Style


def run_test_case(expression, expected_result):
    try:
        lexer = Lexer(expression)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        if expected_result is None:
            print(
                f"{Fore.RED}[FAIL] {expression} → отримано {result}, але очікувалась помилка{Style.RESET_ALL}")
        elif result == expected_result:
            print(f"{Fore.GREEN}[OK] {expression} = {result}{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED}[FAIL] {expression} → {result}, очікувалось: {expected_result}{Style.RESET_ALL}")
    except Exception as e:
        if expected_result is None:
            print(
                f"{Fore.GREEN}[OK] {expression} → очікувана помилка: {e}{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED}[FAIL] {expression} → помилка: {e}, очікувалось: {expected_result}{Style.RESET_ALL}")


def run_all_tests():
    test_cases = [
        ("2 + 3", 5),
        ("10 - 4", 6),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("10 / 2", 5.0),
        ("8 / (2 + 2)", 2.0),
        ("7 + 3 * (10 / (12 / (3 + 1) - 1))", 22.0),
        ("(1 + 2) * (3 + 4)", 21),
        ("(10 - (2 + 3)) * 2", 10),
        ("2 + * 3", None),  # Синтаксис як варіант
        ("(4 + 5", None),  # відсутність дужки
        ("2 + 2", 5),  # неправильний очікуваний результат
        ("2 + 3", None)  # помилка очікується, але її не буде

    ]

    for expr, expected in test_cases:
        run_test_case(expr, expected)
