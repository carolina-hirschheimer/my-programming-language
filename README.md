# Uma Lingagem de Programação
#### Feito por Carolina Hirschheimer

## Introdução
Este projeto faz parte da disciplina de Lógica da Computação (7º Semestre de Engenharia da Computação - Insper) e tem por objetivo que os alunos criem uma linguagem de programação com todas as respectivas estruturas básicas: variáveis, condicionais, loops e funções. Para este projeto, será feita uma linguagem de **programação em português**, com comandos como "imprimir" no lugar do "print" ou "enquanto" no lugar do "while". Veja a EBNF está descrita abaixo:

## EBNF
```
BLOCK = { STATEMENT };
STATEMENT = ( λ | ASSIGNMENT | PRINT | WHILE | IF | FUNCTION | CALL_FUNCTION), "\n" ;
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;

PRINT = "imprimir", "(", OR_EXPRESSION, ")" ;
WHILE = "enquanto", "(",  OR_EXPRESSION, ")", "{", STATEMENT, "}" ;
IF = "se", "(", EXPRESSION, ")", "{", STATEMENT, "}" |
     "se", "(", EXPRESSION, ")", "{", STATEMENT, "}", "senao", "{", STATEMENT, "}" ;

FUNCTION = "definir", IDENTIFIER, "(", [ IDENTIFIER, { ",", IDENTIFIER } ], ")",  "{", { STATEMENT }, "}", RETURN, OR_EXPRESSION;
RETURN = "retorna" OR_EXPRESSION;
CALL_FUNCTION = IDENTIFIER, "(", [ IDENTIFIER, { ",", IDENTIFIER } ], ")";

OR_EXPRESSION = AND_EXPRESSION, {"ou", AND_EXPRESSION};
AND_EXPRESSION = EQUAL_EXPRESSION, {"e", EQUAL_EXPRESSION};
EQUAL_EXPRESSION = COMPARE_EXPRESSION, {"igual_a", COMPARE_EXPRESSION};
COMPARE_EXPRESSION = EXPRESSION, {("maior_que"|"menor_que"), EXPRESSION};
EXPRESSION = TERM, {("+" | "-"), TERM};
TERM = FACTOR, {("*" | "/"), FACTOR};
FACTOR = ("+" | "-", "!"), FACTOR | "(", OR_EXPRESSION, ")" | NUMBER | IDENTIFIER | STRING | BOOLEAN;

IDENTIFIER = TYPE, LETTER, {LETTER | DIGIT | "_"};
NUMBER = DIGIT, {DIGIT};
LETTER = (A | ... | Z | a | ... | z);
DIGIT = (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0);
BOOLEAN = "verdadeiro" | "falso";
STRING = """, { {LETTER | DIGIT | "_"} | SPACE }, """;
SPACE = " ";
TYPE = "int" | "bool" | "texto"
```
