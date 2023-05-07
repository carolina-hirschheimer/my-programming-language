%{
#include <stdio.h>
#include <stdlib.h>
#include "analysis.tab.h"
//extern int yywrap();
%}

%{
#define YYEOF 0
%}

DIGIT [0-9]
LETTER [a-zA-Z]
AND_EXPR and
OR_EXPR or
PRINT imprimir
WHILE enquanto
IF se
ELSE senao
FUNCTION definir
RETURN retorna
EQUAL_EXPR igual_a
COMPARE_EXPR maior_que|menor_que
IDENTIFIER  [a-zA-Z_][_a-zA-Z0-9]*
RECEIVE recebe 
PLUS "+"
MINUS "-"
MULT "*"
DIV "/"
NOT "!"
COMMA ","
BOOLEAN verdadeiro|falso 
TYPE int|bool|texto

%%

"\n"                    { printf("NEWLINE: %s\n", yytext); return NEWLINE; }
{TYPE}                  { printf("TYPE: %s\n", yytext); return TYPE; }
{AND_EXPR}              { printf("AND_EXPR: %s\n", yytext); return AND_EXPR; }
{OR_EXPR}               { printf("OR_EXPR: %s\n", yytext); return OR_EXPR; }
{PRINT}                 { printf("PRINT: %s\n", yytext); return PRINT; }
{WHILE}                 { printf("WHILE: %s\n", yytext); return WHILE; }
{IF}                    { printf("IF: %s\n", yytext); return IF; }
{ELSE}                  { printf("ELSE: %s\n", yytext); return ELSE; }
{FUNCTION}              { printf("FUNCTION: %s\n", yytext); return FUNCTION; }
{RETURN}                { printf("RETURN: %s\n", yytext); return RETURN; }
{EQUAL_EXPR}            { printf("EQUAL_EXPR: %s\n", yytext); return EQUAL_EXPR; }
{RECEIVE}               { printf("RECEIVE: %s\n", yytext); return RECEIVE; }
{COMPARE_EXPR}          { printf("COMPARE_EXPR: %s\n", yytext); return COMPARE_EXPR; }
{PLUS}                  { printf("PLUS: %s\n", yytext); return PLUS; }
{MINUS}                 { printf("MINUS: %s\n", yytext); return MINUS; }
{MULT}                  { printf("MULT: %s\n", yytext); return MULT; }
{DIV}                   { printf("DIV: %s\n", yytext); return DIV; }
{NOT}                   { printf("NOT: %s\n", yytext); return NOT; }
{COMMA}                 { printf("COMMA: %s\n", yytext); return COMMA; }
{BOOLEAN}               { printf("BOOLEAN: %s\n", yytext); return BOOLEAN; }

"("                     { printf("OPEN_PARENTHESIS: %s \n", yytext); return OPEN_PARENTHESIS; }
")"                     { printf("CLOSE_PARENTHESIS: %s \n", yytext); return CLOSE_PARENTHESIS; }
"{"                     { printf("OPEN_BRACES: %s \n", yytext); return OPEN_BRACES; }
"}"                     { printf("CLOSE_BRACES: %s \n", yytext); return CLOSE_BRACES; }


\'([^\\\n]|(\\.))*\'    { printf("STRING: %s\n", yytext); return STRING; }

{IDENTIFIER}                    { printf("IDENTIFIER: %s\n", yytext);  return IDENTIFIER;  }
{DIGIT}+                { printf("INT: %s \n", yytext); return INT; }
{DIGIT}+[.]{DIGIT}+     { printf("FLOAT: %s \n", yytext); return FLOAT; }

[ \t]                   { /* ignore */ }

. { printf("ERRO: %s \n", yytext); return 404; }


%%

int yywrap() {
    return 1;
}

/*
int main()
{
    yylex();
    return 0;
}
*/