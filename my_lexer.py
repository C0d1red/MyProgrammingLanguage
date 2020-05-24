from extra.errors import *
from extra.tokens import *


class Lexer:

    def __init__(self, text):
        self.text = text
        self.current_char = None
        self.position = -1
        self.advance()

    def advance(self):
        self.position += 1
        if self.position < len(self.text):
            # Next char
            self.current_char = self.text[self.position]
        else:
            # End of the text
            self.current_char = None

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t\n':
                # Space or tab
                self.advance()
            elif self.current_char in DIGITS:
                # Make number by digits
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(PLUS_T))
                self.advance()
            elif self.current_char == '-':

                # Check unary minus
                if tokens:
                    if tokens[-1].t_type not in (FLOAT_T, INT_T, FLOAT_UN_T, INT_UN_T, VAR_T):
                        tokens.append(self.make_number())
                    else:
                        tokens.append(Token(MINUS_T))
                        self.advance()
                else:
                    tokens.append(self.make_number())
            elif self.current_char == '*':
                tokens.append(Token(MULT_T))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(DIV_T))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(LRB_T))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(RRB_T))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(LBB_T))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(RBB_T))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(SEMICOLON_T))
                self.advance()
            elif self.current_char == '>':
                tokens.append(Token(MORE_T))
                self.advance()
            elif self.current_char == '<':
                tokens.append(Token(LESS_T))
                self.advance()
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char.isalpha():
                tokens.append(self.make_word())
            else:
                # Return error
                char = self.current_char
                self.advance()
                return [], IllegalCharError('\'' + char + '\'')

        return tokens, None

    def make_word(self):
        word_str = ''

        while self.current_char is not None and self.current_char.isalpha() and self.current_char != ' ':
            word_str += self.current_char
            self.advance()

        if word_str == 'if':
            return Token(IF_T)
        elif word_str == 'while':
            return Token(WHILE_T)
        elif word_str == 'else':
            return Token(ELSE_T)
        elif word_str == 'True':
            return Token(BOOL_T, True)
        elif word_str == 'False':
            return Token(BOOL_T, False)
        else:
            return Token(VAR_T, word_str)

    def make_equals(self):
        equals_count = 1
        self.advance()
        if self.current_char == '=':
            equals_count += 1
            self.advance()

        if equals_count == 2:
            return Token(EQUALS_T)
        else:
            return Token(ASSIGN_T)

    def make_number(self):
        number_str = ''
        dot_count = 0
        minus_count = 0

        ad_chars = '.-'

        while self.current_char is not None and self.current_char in DIGITS + ad_chars:
            ad_chars = '.'

            if self.current_char == '.':

                # One number have one dot
                if dot_count == 1:
                    break

                dot_count += 1

            elif self.current_char == '-':

                # One number have one dot
                if minus_count == 1:
                    break

                minus_count += 1
            number_str += self.current_char
            self.advance()

        if dot_count > 0:
            if minus_count > 0:
                return Token(FLOAT_UN_T, float(number_str))
            else:
                return Token(FLOAT_T, float(number_str))
        else:
            if minus_count > 0:
                return Token(INT_UN_T, int(number_str))
            else:
                return Token(INT_T, int(number_str))


def run(text):
    lexer = Lexer(text)
    tokens, errors = lexer.make_tokens()
    return tokens, errors
