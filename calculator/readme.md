## Simple Calculator

To use the simple calculator, follow these steps:

1. Move to the directory of the simple calculator: `cd simpleCalculator`
2. Get the header (`parse.tab.h`) file containing tokens using the command: `yacc -d parse.y`
3. Compile the lex to get `lex.yy.c` file using the command: `lex lex.l`
4. Compile the yacc program to get `parse.tab.c` using the command: `yacc parse.y`
5. Get the executable file `parser.out` using the command: `gcc parse.tab.c -o parser`
6. Run the program using the command: `./parser`

## Enhanced Calculator

The enhanced calculator supports two more operators (modulo and exponentiation) with bracket support. To use it, follow these steps:

1. Move to the directory of the enhanced calculator: `cd enhancedCalculator`
2. Get the header (`parse.tab.h`) file containing tokens using the command: `yacc -d parse.y`
3. Compile the lex to get `lex.yy.c` file using the command: `lex lex.l`
4. Compile the yacc program to get `parse.tab.c` using the command: `yacc parse.y`
5. Get the executable file `parser.exe` using the command: `gcc parse.tab.c -o parser`
6. Run the program using the command: `./parser`

