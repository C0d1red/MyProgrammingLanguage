from extra.tokens import *
from extra.errors import InvalidSyntaxError


class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return str(self.token)


class BinOpNode:
    def __init__(self, left_n, op_token, right_n):
        self.left_n = left_n
        self.op_token = op_token
        self.right_n = right_n

    def __repr__(self):
        return f'({self.left_n}, {self.op_token}, {self.right_n})'


class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f'{self.op_token}, {self.node}'


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self):
        return self.expression()

    def expression(self):
        return self.binary_op(self.term, (PLUS_T, MINUS_T))

    def term(self):
        return self.binary_op(self.factor, (MULT_T, DIV_T))

    def factor(self):
        res = ParseResult()
        token = self.current_token

        if token.t_type in (MINUS_T, PLUS_T):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res.error
            else:
                return res.success(UnaryOpNode(token, factor))
        elif token.t_type in (INT_T, FLOAT_T, INT_UN_T, FLOAT_UN_T):
            res.register(self.advance())
            return res.success(NumberNode(token))
        elif token.t_type in (RRB_T, LRB_T):
            res.register(self.advance())
            expr = res.register(self.expression())
            if res.error:
                return res.error
            if self.current_token.t_type == RRB_T:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError("Expected ')'"))

        return res.failure(InvalidSyntaxError("Expected INT or FLOAT"))

    def binary_op(self, rule_func, ops):
        res = ParseResult()
        left = res.register(rule_func())
        if res.error:
            return res
#
        while self.current_token.t_type in ops:
            op_token = self.current_token
            res.register(self.advance())
            right = res.register(rule_func())
            if res.error:
                return res
            left = BinOpNode(left, op_token, right)
        return res.success(left)


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


def run(tokens):
    parser = Parser(tokens)
    result = parser.parse()

    return result.node, result.error
