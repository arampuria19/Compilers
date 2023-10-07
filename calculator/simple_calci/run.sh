#!/bin/zsh

# Compile parse.y using yacc
yacc parse.y -d

# Compile tokenizer.l using lex
lex lex.l

# Compile parse.tab.c using g++
g++ y.tab.c -o parser

# Execute the parser
./parser
