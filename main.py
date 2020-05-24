import my_lexer
import my_parser
import my_rpn
import my_stack_machine

file = open("code_example")
text = file.read()

tokens, token_errors = my_lexer.run(text)
print('Tokens:')
if token_errors:
    print(token_errors)
else:
    print(tokens)

poliz_result = my_rpn.run(tokens)
print('\nRPN:')
print(poliz_result)

machine_result = my_stack_machine.run(poliz_result)
print('\nStack-machine (result variables):')
print(machine_result)
