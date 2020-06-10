from extra.tokens import *
from extra.my_stack import Stack


# Operations priority
PRIORITY = {
    LRB_T: 0,
    ASSIGN_T: 0,
    MORE_T: 1,
    LESS_T: 1,
    PLUS_T: 1,
    MINUS_T: 1,
    DIV_T: 2,
    MULT_T: 2,
    EQUALS_T: 2,
    LL_T: 0,
    HT_T: 0
}


class RPN:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = Stack()
        self.result = []
        self.token_index = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def translate(self):
        while self.token_index < len(self.tokens):
            if self.current_token.t_type == IF_T:
                self.result += self.make_if_rpn()
            elif self.current_token.t_type == WHILE_T:
                self.result += self.make_while_rpn()
            else:
                self.result += self.make_term_rpn(SEMICOLON_T)

        return self.result

    def make_if_rpn(self):
        if_result = []
        if_result += self.make_conditional_part()
        if_result += self.make_body_rpn()

        ##########################
        # Set go_to
        ##########################

        # Go_to by false
        go_false_pos = len(if_result) + len(self.result) + 1
        for i in range(len(if_result)):
            if if_result[i].t_type in GO_FALSE:
                if_result[i] = Token(GO_FALSE, go_false_pos)

        # Go_to by absolute
        if_result.append(Token(GO_ABSOLUTE, -1))

        #########################
        # Else section
        #########################
        if self.current_token.t_type in ELSE_T:
            if_result += self.make_body_rpn()

        go_absolute_pos = len(if_result) + len(self.result)
        for i in range(len(if_result)):
            if if_result[i].t_type in GO_ABSOLUTE:
                if_result[i] = Token(GO_ABSOLUTE, go_absolute_pos)

        return if_result

    def make_while_rpn(self):
        while_result = []
        while_result += self.make_conditional_part()
        while_result += self.make_body_rpn()

        ##########################
        # Set go_to
        ##########################

        # Go_to by false
        go_false_pos = len(while_result) + len(self.result) + 1
        for i in range(len(while_result)):
            if while_result[i].t_type in GO_FALSE:
                while_result[i] = Token(GO_FALSE, go_false_pos)

        # Go_to by absolute
        while_result.append(Token(GO_ABSOLUTE, -1))
        go_absolute_pos = len(self.result)
        for i in range(len(while_result)):
            if while_result[i].t_type in GO_ABSOLUTE:
                while_result[i] = Token(GO_ABSOLUTE, go_absolute_pos)

        return while_result

    def make_conditional_part(self):
        conditional_result = []

        # Advance to the logical term
        self.advance()
        self.advance()

        conditional_result += self.make_term_rpn(RRB_T)

        # Set go_to by false
        conditional_result.append(Token(GO_FALSE, -1))

        return conditional_result

    def make_func_rpn(self):
        func_result = []

        self.advance()
        op = self.current_token
        self.advance()

        while self.current_token.t_type not in RRB_T:
            self.advance()
            func_result += self.make_func_arg()

        func_result.append(op)
        return func_result

    def make_body_rpn(self):
        body_result = []
        while self.current_token.t_type not in RBB_T:

            body_result += self.make_term_rpn(SEMICOLON_T)

        # Delete RBB
        self.advance()

        return body_result

    def make_term_rpn(self, stop_token):
        body_res = []
        body_stack = Stack()
        while self.current_token.t_type not in stop_token:
            # If number or var: write to the body_result
            if self.current_token.t_type in (INT_T, FLOAT_T, INT_UN_T, FLOAT_UN_T, BOOL_T, VAR_T):
                body_res.append(self.current_token)

            # If operation: check priority
            elif self.current_token.t_type in (MINUS_T, PLUS_T, DIV_T, MULT_T, ASSIGN_T, EQUALS_T, MORE_T, LESS_T,
                                               LL_T, HT_T):

                # If stack is empty: push to the stack
                if body_stack.is_empty():
                    body_stack.push(self.current_token)

                # If stack isn't empty
                else:
                    # Priority of the top of stack
                    stack_pr = PRIORITY.get(body_stack.peek().t_type)

                    # Priority of the current operation
                    current_pr = PRIORITY.get(self.current_token.t_type)

                    # While priority on the top of stack not less then new operation
                    while stack_pr >= current_pr:
                        body_res.append(body_stack.pop())
                        if body_stack.is_empty():
                            break
                        else:
                            stack_pr = PRIORITY.get(body_stack.peek().t_type)

                    # Push element to the stack
                    body_stack.push(self.current_token)

            elif self.current_token.t_type in DOT_T:
                body_res += self.make_func_rpn()
                while not body_stack.is_empty():
                    body_res.append(body_stack.pop())

            # If LRB
            elif self.current_token.t_type == LRB_T:

                # Push element to the stack
                body_stack.push(self.current_token)

            # If RRB
            elif self.current_token.t_type == RRB_T:

                # Pop all elements before LRB
                while body_stack.peek().t_type != LRB_T:
                    body_res.append(body_stack.pop())

                # Deleting LRB
                body_stack.pop()
            self.advance()

        self.advance()

        # Pop all from the stack
        while not body_stack.is_empty():
            body_res.append(body_stack.pop())
        return body_res

    def make_func_arg(self):
        func_res = []
        func_stack = Stack()
        while self.current_token.t_type not in (COMMA_T, RRB_T):

            # If number or var: write to the body_result
            if self.current_token.t_type in (INT_T, FLOAT_T, INT_UN_T, FLOAT_UN_T, BOOL_T, VAR_T):
                func_res.append(self.current_token)

            # If operation: check priority
            elif self.current_token.t_type in (MINUS_T, PLUS_T, DIV_T, MULT_T, ASSIGN_T, EQUALS_T, MORE_T, LESS_T,
                                               LL_T, HT_T):

                # If stack is empty: push to the stack
                if func_stack.is_empty():
                    func_stack.push(self.current_token)

                # If stack isn't empty
                else:
                    # Priority of the top of stack
                    stack_pr = PRIORITY.get(func_stack.peek().t_type)

                    # Priority of the current operation
                    current_pr = PRIORITY.get(self.current_token.t_type)

                    # While priority on the top of stack not less then new operation
                    while stack_pr >= current_pr:
                        func_res.append(func_stack.pop())
                        if func_stack.is_empty():
                            break
                        else:
                            stack_pr = PRIORITY.get(func_stack.peek().t_type)

                    # Push element to the stack
                    func_stack.push(self.current_token)

            elif self.current_token.t_type in DOT_T:
                func_res += self.make_func_rpn()
                while not func_stack.is_empty():
                    func_res.append(func_stack.pop())

            self.advance()

        # Pop all from the stack
        while not func_stack.is_empty():
            func_res.append(func_stack.pop())
        return func_res


def run(tokens):
    rpn = RPN(tokens)
    res = rpn.translate()
    return res
