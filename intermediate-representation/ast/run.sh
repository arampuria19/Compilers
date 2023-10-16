#!/bin/zsh

# Compile parse.y
yacc parse.y -d

# Compile lex.l
flex lex.l

# Compile the generated C code
g++ y.tab.c -o ast

./ast
