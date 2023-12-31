%{
    #include <iostream>
    #include <cmath> 
    #include "lex.yy.c"
    using namespace std;
    bool flag = false;
    bool divideByZeroException = false;
    void yyerror(const char *str);
%}

%token DIV INTCONST MINUS MULT PLUS LEFTPAREN RIGHTPAREN POWER MOD

%left PLUS MINUS
%left MULT DIV MOD

%start S

%%

S: E { 
    if(!divideByZeroException)
        printf("Answer = %d\n", $$); 
    return 0;
};

E: E PLUS T {$$ = $1 + $3;}
| E MINUS T {$$ = $1 - $3;}
| T 
;

T: T MULT P {$$ = $1 * $3;}
| T DIV P   
{
    if($3 != 0)
        $$ = $1 / $3;
    else {
        divideByZeroException = true;
    }
}
| T MOD P 
{
    if($3 != 0)
        $$ = $1 % $3;
    else {
        divideByZeroException = true;
    }
}
| P
;

P: P POWER F {$$ = (int)(pow($1, $3) + 1e-9);} 
| F
;

F: LEFTPAREN E RIGHTPAREN {$$ = $2;}
| INTCONST {$$ = $1;}
;

%%


int main() 
{ 
    yyin = fopen("input.txt", "r");
    yyparse();
    if(!flag)
	    printf("Entered arithmetic expression is Valid.\n"); 
    if(divideByZeroException) 
        printf("Divide By Zero Exception");
    return 0;
} 

void yyerror(const char *str) { 
	printf("Entered arithmetic expression is Invalid.\n"); 
    flag = true; 
} 
