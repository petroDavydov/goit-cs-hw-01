from lexer_analyzer import TokenType, Token

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