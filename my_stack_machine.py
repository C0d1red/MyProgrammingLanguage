from extra.my_stack import Stack
from extra.tokens import *
from extra.linked_list import *
from extra.hash_table import *

# Variables dictionary
VARIABLES = {}


class StackMachine:
    def __init__(self, elements):
        self.elements = elements
        self.stack = Stack()
        self.result = []
        self.element_index = -1
        self.current_element = None
        self.advance()

    def advance(self):
        self.element_index += 1
        if self.element_index < len(self.elements):
            self.current_element = self.elements[self.element_index]
        else:
            self.current_element = None
        return self.current_element

    def calculate(self):
        while self.current_element is not None:

            # If element is number or var or bool: push into stack
            if self.current_element.t_type in (FLOAT_T, INT_T, FLOAT_UN_T, INT_UN_T, VAR_T, BOOL_T):
                self.stack.push(self.current_element)

            # If element is operation
            elif self.current_element.t_type in (ASSIGN_T, EQUALS_T, LESS_T, MORE_T, PLUS_T, MINUS_T, MULT_T, DIV_T):

                # Operation
                op = self.current_element.t_type

                # Element 1
                el1 = self.stack.pop()

                # Element 2
                el2 = self.stack.pop()

                # If operation is assignment
                if op in ASSIGN_T:
                    self.assign_op(el1, el2)
                else:

                    # Checking variable for value
                    if el1.t_type in VAR_T:
                        el1 = VARIABLES.get(el1.value)
                    if el2.t_type in VAR_T:
                        el2 = VARIABLES.get(el2.value)

                    # Logical operation
                    if op in (EQUALS_T, LESS_T, MORE_T):
                        self.stack.push(self.logical_op(el1, el2))

                    # Arithmetic operation
                    if op in (PLUS_T, MINUS_T, MULT_T, DIV_T):
                        self.stack.push(self.arith_op(el1, el2))

            elif self.current_element.t_type in LL_T:
                # Element 2
                el = self.stack.pop()

                VARIABLES[el.value] = Linkedlist()

            elif self.current_element.t_type in HT_T:
                # Element 2
                el = self.stack.pop()
                VARIABLES[el.value] = HashTable()


            elif self.current_element.t_type in (ADD_T, GET_T, SIZE_T, ADDF_T):
                self.ll_op(self.current_element.t_type)


            elif self.current_element.t_type in (PUT_T, CONTAIN_T, GETV_T):
                self.ht_op(self.current_element.t_type)


            # If GO_FALSE
            elif self.current_element.t_type in GO_FALSE:

                # Checking variable for value
                value = self.stack.pop()

                if value.t_type in VAR_T:
                    value = VARIABLES.get(value.value)
                    value = value.value
                else:
                    value = value.value

                # If top of the stack is False: go to index_value of GO_FALSE
                if value is False:
                    self.element_index = self.current_element.value - 1

            # If GO_ABSOLUTE: go to index_value of GO_ABSOLUTE
            elif self.current_element.t_type in GO_ABSOLUTE:
                self.element_index = self.current_element.value - 1

            self.advance()

        return VARIABLES

    def assign_op(self, el1, el2):
        VARIABLES[el2.value] = el1

    def logical_op(self, el1, el2):
        result = None

        if self.current_element.t_type in EQUALS_T:
            result = el2.value == el1.value
        elif self.current_element.t_type in LESS_T:
            result = el2.value < el1.value

        elif self.current_element.t_type in MORE_T:
            result = el2.value > el1.value

        return Token(BOOL_T, result)

    def arith_op(self, el1, el2):
        result = None

        if self.current_element.t_type in PLUS_T:
            result = el2.value + el1.value
        elif self.current_element.t_type in MINUS_T:
            result = el2.value - el1.value
        elif self.current_element.t_type in MULT_T:
            result = el2.value * el1.value
        elif self.current_element.t_type in DIV_T:
            result = el2.value / el1.value

        return Token(INT_T, result)

    def ll_op(self, op):

        if op in ADD_T:
            # Element 1
            num_el = self.stack.pop()

            # Element 2
            var_el = self.stack.pop()
            VARIABLES[var_el.value].add(num_el)
        elif op in GET_T:
            # Element 1
            num_el = self.stack.pop()

            # Element 2
            var_el = self.stack.pop()
            self.stack.push(VARIABLES[var_el.value].get_at(num_el.value))
        elif op in ADDF_T:
            # Element 1
            num_el = self.stack.pop()

            # Element 2
            var_el = self.stack.pop()
            VARIABLES[var_el.value].add(num_el)
        elif op in SIZE_T:
            # Element 1
            num_el = self.stack.pop()
            self.stack.push(Token(INT_T, VARIABLES[num_el.value].size()))

    def ht_op(self, op):

        if op in PUT_T:
            # Elements
            num_el_value = self.stack.pop()
            num_el_key = self.stack.pop()

            # Element 2
            var_el = self.stack.pop()
            VARIABLES[var_el.value].put(num_el_key.value, num_el_value.value)
        elif op in GETV_T:
            # Element 1
            num_el = self.stack.pop()

            # Element 2
            var_el = self.stack.pop()
            self.stack.push(Token(INT_T, VARIABLES[var_el.value].get_value(num_el.value)))
        elif op in CONTAIN_T:
            # Element 1
            num_el = self.stack.pop()

            # Element 2
            var_el = self.stack.pop()
            self.stack.push(Token(BOOL_T, VARIABLES[var_el.value].contain(num_el.value)))


def run(tokens):
    stack_machine = StackMachine(tokens)
    result = stack_machine.calculate()

    return result
