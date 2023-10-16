#!/bin/zsh

# Compile parse.y
yacc parse.y -d

# Compile lex.l
lex lex.l

# Compile the generated C code
g++ y.tab.c -o 3ac

./3ac