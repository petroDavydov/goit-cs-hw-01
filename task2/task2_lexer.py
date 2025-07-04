from colorama import Fore, Style, init
init(autoreset=True)


class LexicalError(Exception):
    pass


class ParsingError(Exception):
    pass


class TokenType:
    INTEGER = "INTEGER"
    PLUS = "PLUS"  # Додавання
    MINUS = "MINUS"  # Віднімання
    MUL = "MUL"  # Множення
    DIV = "DIV"  # Ділення
    LPAREN = "LPAREN"  # Ліва дужка
    RPAREN = "RPAREN"  # Права дужка
    EOF = "EOF"  # Означає кінець вхідного рядка


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        """Переміщуємо 'вказівник' на наступний символ вхідного рядка"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Означає кінець введення
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Пропускаємо пробільні символи."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Повертаємо ціле число, зібране з послідовності цифр."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Лексичний аналізатор, що розбиває вхідний рядок на токени."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return Token(TokenType.MUL, "*")

            if self.current_char == "/":
                self.advance()
                return Token(TokenType.DIV, "/")

            if self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAREN, ")")

            raise LexicalError("Помилка лексичного аналізу")

        return Token(TokenType.EOF, None)


class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise ParsingError("Помилка синтаксичного аналізу")

    def eat(self, token_type):
        """
        Порівнюємо поточний токен з очікуваним токеном і, якщо вони збігаються,
        'поглинаємо' його і переходимо до наступного токена.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """Парсер для 'factor' правил граматики. У нашому випадку - це цілі числа."""
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.expr()
            self.eat(TokenType.RPAREN)
            return result

    def term(self):
        """Парсер для 'term' включно множення та ділення"""
        node = self.factor()

        while self.current_token.type in (TokenType.DIV, TokenType.MUL):
            token = self.current_token
            if token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            elif token.type == TokenType.MUL:
                self.eat(TokenType.MUL)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """Парсер для арифметичних виразів."""
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node


def print_ast(node, level=0):
    indent = "  " * level
    if isinstance(node, Num):
        print(f"{indent}Num({node.value})")
    elif isinstance(node, BinOp):
        print(f"{indent}BinOp:")
        print(f"{indent}  left: ")
        print_ast(node.left, level + 2)
        print(f"{indent}  op: {node.op.type}")
        print(f"{indent}  right: ")
        print_ast(node.right, level + 2)
    else:
        print(f"{indent}Unknown node type: {type(node)}")


class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    # якщо буде // то буде ціле число
    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.type == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"Немає методу visit_{type(node).__name__}")


# для автоматичного тестування
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


# додано строку для визову тесту
def main():
    while True:
        try:
            text = input(
                f'{Fore.CYAN}Введіть вираз (або{Fore.LIGHTRED_EX} "exit" для виходу, {Fore.LIGHTYELLOW_EX}"test" для тестів): {Style.RESET_ALL}')
            if text.lower() == "exit":
                print(
                    f"{Fore.BLUE}🙏 за користування! Допобачення. 👣 із програми.{Style.RESET_ALL}")
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
