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


LL_T = 'LINKED_LIST'
HT_T = 'HASH_TABLE'
DOT_T = 'DOT'
COMMA_T = 'COMMA'

INSERT_T = 'INSERT'
ADD_T = 'ADD'
ADDF_T = 'ADD_F'
GET_T = 'GET'
SIZE_T = 'SIZE'

PUT_T = 'PUT'
CONTAIN_T = 'CONTAIN'
GETV_T = 'GET_V'


class Token:

    def __init__(self, t_type, value=None):
        self.t_type = t_type
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return str(self.t_type) + ':' + str(self.value)
        return str(self.t_type)
