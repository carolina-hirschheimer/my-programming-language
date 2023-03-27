# Uma Lingagem de Programação
#### Feito por Carolina Hirschheimer

## Introdução 

## EBNF
```
BLOCK = { STATEMENT };
STATEMENT = ( λ | ASSIGNMENT | PRINT | WHILE | IF | FUNCTION), "\n" ;
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;

PRINT = "imprimir", "(", OR_EXPRESSION, ")" ;
WHILE = "enquanto", "(",  OR_EXPRESSION, ")", "{", STATEMENT, "}" ;
IF = "se", "(", EXPRESSION, ")", "{", STATEMENT, "}" |
     "se", "(", EXPRESSION, ")", "{", STATEMENT, "}", "senao", "{", STATEMENT, "}" ;

FUNCTION = "definir", IDENTIFIER, "(", [ IDENTIFIER, { ",", IDENTIFIER } ], ")",  "{", { STATEMENT }, "}", RETURN;
RETURN = "retorna" OR_EXPRESSION;

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
