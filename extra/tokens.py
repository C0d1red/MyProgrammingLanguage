# All digits in the language
DIGITS = '0123456789'


################################
# TOKENS
#################################

VAR_T = 'VAR'
INT_T = 'INT'
FLOAT_T = 'FLOAT'
INT_UN_T = 'UN_INT'
FLOAT_UN_T = 'UN_FLOAT'
BOOL_T = 'BOOL'


PLUS_T = 'PLUS'
MINUS_T = 'MINUS'
MULT_T = 'MULT'
DIV_T = 'DIV'


# Brackets
LRB_T = 'LRB'
RRB_T = 'RRB'
LBB_T = 'LBB'
RBB_T = 'RBB'


SEMICOLON_T = 'SEMICOLON'


WHILE_T = 'WHILE'
IF_T = 'IF'
ELSE_T = 'ELSE'
EQUALS_T = 'EQUALS'
LESS_T = 'LESS'
MORE_T = 'MORE'
ASSIGN_T = 'ASSIGN'


GO_ABSOLUTE = 'GO_ABSOLUTE'
GO_FALSE = 'GO_FALSE'


class Token:

    def __init__(self, t_type, value=None):
        self.t_type = t_type
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return str(self.t_type) + ':' + str(self.value)
        return str(self.t_type)
