%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int yylex();
void yyerror(const char *s) { printf("ERROR: %s\n", s); }

%}

%token TYPE AND_EXPR OR_EXPR PRINT WHILE IF FUNCTION RETURN EQUAL_EXPR COMPARE_EXPR PLUS MINUS MULT DIV COMMA NOT BOOLEAN
%token OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_BRACES CLOSE_BRACES NEWLINE
%token IDENTIFIER INT FLOAT STRING

%start program

%%

program : statement_list 
        ;

block : statement_list
      ;
        
statement_list : statement
               | statement_list statement
               ;
        
statement : POSITION IDENTIFIER COLON relexpression
          | IDENTIFIER EQUAL relexpression
          | PRINT LPAREN print_list RPAREN
          | IF LPAREN relexpression RPAREN block
          | IF LPAREN relexpression RPAREN block ELSE block
          | WHILE LPAREN relexpression RPAREN block 
          | FUNCTION_DECLARATION IDENTIFIER LPAREN parameter_list RPAREN block
          | FUNCTION_CALL IDENTIFIER LPAREN parameter_list RPAREN
          | SHOOT relexpression
          ;

parameter_list : IDENTIFIER
               | parameter_list COMMA IDENTIFIER
               ;

print_list : relexpression
           | print_list COMMA relexpression
           ;

relexpression: expression EQUAL_TO expression
             | expression GT expression
             | expression LT expression
             | expression
             ;

// ok
expression: term PLUS term
          | term MINUS term
          | term OR term
          | term
          ;

// ok          
term: factor
    | term MULT factor
    | term DIV factor
    | term AND factor
    ;


factor: INTEGER 
    | STRING 
    | COORDINATE
    | IDENTIFIER 
    | PLUS factor
    | MINUS factor
    | NOT factor
    | LPAREN relexpression RPAREN
    ;


%%

int main(){
  yyparse();
  return 0;
}