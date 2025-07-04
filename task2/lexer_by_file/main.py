from lexer_analyzer import Lexer
from parser import Parser
from interpreter import Interpreter
from test_for_lexer import run_all_tests
from colorama import Fore, Style


def main():
    while True:
        try:
            text = input(
                f'{Fore.CYAN}Введіть вираз (або{Fore.LIGHTRED_EX} "exit" для виходу, {Fore.LIGHTYELLOW_EX}"test" для тестів): {Style.RESET_ALL}')
            if text.lower() == "exit":
                print(
                    f"{Fore.LIGHTBLUE_EX}🙏 за користування! Допобачення. 👣 із програми.{Style.RESET_ALL}")
                break
            elif text.lower() == "test":
                run_all_tests()
                continue
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(f"{Fore.LIGHTGREEN_EX}{result}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
