%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int yylex();
void yyerror(const char *s) { printf("ERROR: %s\n", s); }

%}

%token TYPE AND_EXPR OR_EXPR PRINT WHILE IF ELSE FUNCTION RETURN EQUAL_EXPR RECEIVE COMPARE_EXPR PLUS MINUS MULT DIV COMMA NOT BOOLEAN
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
        
statement : TYPE IDENTIFIER relexpression
          | IDENTIFIER RECEIVE relexpression
          | PRINT OPEN_PARENTHESIS print_list CLOSE_PARENTHESIS
          | IF OPEN_PARENTHESIS relexpression CLOSE_PARENTHESIS block
          | IF OPEN_PARENTHESIS relexpression CLOSE_PARENTHESIS block ELSE block
          | WHILE OPEN_PARENTHESIS relexpression CLOSE_PARENTHESIS block 
          | FUNCTION IDENTIFIER OPEN_PARENTHESIS parameter_list CLOSE_PARENTHESIS block
          | IDENTIFIER OPEN_PARENTHESIS parameter_list CLOSE_PARENTHESIS
          ;

parameter_list : IDENTIFIER
               | parameter_list COMMA IDENTIFIER
               ;

print_list : relexpression
           | print_list COMMA relexpression
           ;

relexpression: expression EQUAL_EXPR expression
             | expression COMPARE_EXPR expression
             | expression
             ;

// ok
expression: term PLUS term
          | term MINUS term
          | term OR_EXPR term
          | term
          ;

// ok          
term: factor
    | term MULT factor
    | term DIV factor
    | term AND_EXPR factor
    ;


factor: INT 
    | STRING 
    | IDENTIFIER 
    | PLUS factor
    | MINUS factor
    | NOT factor
    | OPEN_PARENTHESIS relexpression CLOSE_PARENTHESIS
    ;


%%

int main(){
  yyparse();
  return 0;
}