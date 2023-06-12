import sys

string = sys.argv[1]

class Token():
    def __init__(self, value, type):
        self.value = value
        self.type = type

class PrePro():
    def __init__(self, source):
        self.source = source

    @staticmethod
    def filter(source):
        source = source.split("\n")
        for i in range(len(source)):
            source[i] = source[i].split("#")[0]
            source[i] = source[i].strip()
        source = "\n".join(source)

        return source

class Tokenizer():

    def __init__(self, source):
        self.source = source #código-fonte que será tokenizado (string)
        self.position = 0 #posição atual que o Tokenizador está separando (integer)
        self.next = None #o último token separado (Token)

    def selectNext(self): # lê o próximo token e atualiza o atributo next

        number_tokens = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        letters_tokens = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        operation_tokens = ['+', '-', '*', '/', '(', ')', '=', '\n', '>', '<', '!', '|', '&', ':', '.', ',']
        reserved_words = ['println', 'if', 'else', 'while', 'readline', '||', '&&', 'end', '==', "Int", "String", "return", "function"]

        walking_in_string = True

        # Checa se a string já acabou, ou se conseguimos pegar o próximo
        try:
            i = self.source[self.position]
        except:
            #print("bom diaaa")
            self.next = Token('','EOF')
            return
        
        # Se string não acabou, checa o tipo do caracter: (i) se é operação
        if i in operation_tokens:
            if i == '+':
                self.next = Token(i, 'PLUS')
            if i == '-':
                self.next = Token(i, 'MINUS')
            if i == '*':
                self.next = Token(i, 'MULT')
            if i == '/':
                self.next = Token(i, 'DIV')
            if i == '(':
                self.next = Token(i, 'PAREN')
            if i == ')':
                self.next = Token(i, 'PAREN')
            elif i == "=":
                if self.source[self.position + 1] == "=":
                    #print("consigo ler")
                    self.next = Token("==", "EQEQUALS")
                    self.position += 1
                else:
                    self.next = Token(i, 'EQUALS')
            if i == '\n':
                self.next = Token(i, 'ENTER')
                #print("blaa1")
            if i == '>':
                self.next = Token(i, 'GREATER')
            if i == '<':
                self.next = Token(i, 'LESS')
                #print("asdf")
            if i == '!':
                self.next = Token(i, 'NOT')
            if i == "|":
                if self.source[self.position + 1] == "|":
                    self.next = Token('||', 'OR')
                    self.position += 1
                else:
                    raise Exception("Erro Lexico")
            if i == "&":
                if self.source[self.position + 1] == "&":
                    #print("blaaa")
                    self.next = Token('&&', 'AND')
                    self.position += 1
                else:
                    raise Exception("Erro Lexico")
            if i == ":":
                if self.source[self.position + 1] == ":":
                    self.next = Token("::", "DECLARE")
                    self.position+=1
                else:
                    raise Exception("Erro Lexico")
            if i == ".":
                self.next = Token(i, "CONCAT")
            if i == ",":
                self.next = Token(i, "COMMA")
            
            self.position += 1
            return 
        
        # Se string não acabou, checa o tipo do caracter: (ii) se é número
        elif i in number_tokens:
            number_string = ''
            number_string += i

            while walking_in_string:
                self.position+=1
                try:
                    i = self.source[self.position]
                except:
                    self.next = Token(int(number_string),'INT')
                    return
                
                if (i == ' ') or (i in operation_tokens):
                    walking_in_string = False
                    self.next = Token(int(number_string),'INT')
                else:
                    number_string += i
            
        elif i in letters_tokens:
            word_string = ''
            word_string += i

            while walking_in_string:
                self.position+=1
                try:
                    i = self.source[self.position]
                except:
                    self.next = Token(word_string,'ID')
                    return
                
                if (i == ' ') or (i in operation_tokens):
                    walking_in_string = False
                    if word_string in reserved_words:
                        if word_string == "Int" or word_string == "String":
                            self.next = Token(word_string, "TYPE")
                        else:
                            self.next = Token(word_string, word_string.upper())
                    else:
                        self.next = Token(word_string,'ID')
                else:
                    word_string += i

        elif i == '"':
            word_string = ''

            while walking_in_string:
                self.position+=1
                try:
                    i = self.source[self.position]
                    if i == '"':
                        walking_in_string = False
                    else:
                        word_string += i
                except:
                    raise Exception("quotation mark unclosed")
                
            self.position += 1
            self.next = Token(word_string, "STRING")

        # Se string não acabou, checa o tipo do caracter: (iii) se é espaço
        elif i == ' ':
            self.position += 1
            self.selectNext()

class Node():
    def __init__(self, value, children):
        self.value = value # variant
        self.children = children # list of nodes 

    def evaluate(self):
        pass


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,table):
        #child_value = self.children[0].evaluate()
        #print("unop child_value:", child_value)
        if self.value == "-":
            return ("Int",-1 * self.children[0].evaluate(table)[1])
        
        elif self.value == "+":
            return ("Int",self.children[0].evaluate(table)[1])
        
        elif self.value == "!":
            return ("Int",not self.children[0].evaluate(table)[1])

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, table):
        #child_value = self.children[0].evaluate()
        #print("binop child_value:", child_value)
        if self.value == ".":
            return ("String", str(self.children[0].evaluate(table)[1]) + str(self.children[1].evaluate(table)[1]))
        
        else:
            #print("self.children[0].evaluate(): ", self.children[0].evaluate())
            #print("self.children[0].evaluate()[0]: ", self.children[0].evaluate()[0])
            #print("self.children[1].evaluate(): ", self.children[1].evaluate())
            #print("self.children[1].evaluate()[0]: ", self.children[1].evaluate()[0])

            if (self.children[0].evaluate(table)[0] == "Int") and (self.children[1].evaluate(table)[0] == "Int"):

                if self.value == "-":
                    return ("Int", self.children[0].evaluate(table)[1] - self.children[1].evaluate(table)[1])
                elif self.value == "+":
                    return ("Int", self.children[0].evaluate(table)[1] + self.children[1].evaluate(table)[1])
                elif self.value == "*":
                    return ("Int", self.children[0].evaluate(table)[1] * self.children[1].evaluate(table)[1])
                elif self.value == "/":
                    return ("Int", int(self.children[0].evaluate(table)[1] // self.children[1].evaluate(table)[1]))
                elif self.value == '||':
                    return ("Int", int(self.children[0].evaluate(table)[1] or self.children[1].evaluate(table)[1]))
                elif self.value == '&&':
                    return ("Int", int(self.children[0].evaluate(table)[1] and self.children[1].evaluate(table)[1]))
                elif self.value == '==':
                    return ("Int", int(self.children[0].evaluate(table)[1] == self.children[1].evaluate(table)[1]))
                elif self.value == '>':
                    return ("Int", int(self.children[0].evaluate(table)[1] > self.children[1].evaluate(table)[1]))
                elif self.value == '<':
                    return ("Int", int(self.children[0].evaluate(table)[1] < self.children[1].evaluate(table)[1]))
            
            else:
                if self.value == '==':
                    return ("Int", int(self.children[0].evaluate(table)[1] == self.children[1].evaluate(table)[1]))
                elif self.value == '>':
                    return ("Int", int(self.children[0].evaluate(table)[1] > self.children[1].evaluate(table)[1]))
                elif self.value == '<':
                    return ("Int", int(self.children[0].evaluate(table)[1] < self.children[1].evaluate(table)[1]))
                else:
                    raise Exception("type attribution error")
        
        
class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, table):
        return ("Int", self.value)

class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, table):
        return ("String", self.value)
    
class VarDeclaration(Node):
    def __init__(self, value ,children):
        super().__init__(value, children)
        
    def evaluate(self, table):
        table.create(self.children[0].value, self.value)
        table.setter(self.children[0].value, self.children[1].evaluate(table))

class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

    def evaluate(self, table):
        pass

class Block(Node):
    def __init__ (self, children):
        super().__init__(None, children)
    
    def evaluate(self, table):
        for child in self.children:
            #print(child.value)
            if child.value == "return":
                return child.evaluate(table)
            child.evaluate(table)

class Identifier(Node):
    def __init__ (self, value):
        super().__init__(value, [])
    
    def evaluate(self, table):
        return table.getter(self.value)

class Println(Node):
    def __init__ (self, children):
        super().__init__(None, children)

    def evaluate(self, table):
        print(self.children[0].evaluate(table)[1])

class Readln(Node):
    def __init__ (self, children):
        super().__init__(None, children)

    def evaluate(self, table):
        return ("Int", int(input()))
    
class While(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, table):
        #child_value = self.children[0].evaluate()
        #print("while child_value:", child_value)
        while self.children[0].evaluate(table)[1]:
            self.children[1].evaluate(table)

class If(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, table):
        #child_value = self.children[0].evaluate()
        #print("if child_value:", child_value)
        if len(self.children) == 2:
            if self.children[0].evaluate(table)[1]:
                self.children[1].evaluate(table)
        else:
            #print("self.children[0]: ", self.children[0])
            #print("self.children[1]: ", self.children[1])
            #print("self.children[0].evaluate(): ", self.children[0].evaluate())
            #print("self.children[0].evaluate()[1]: ", self.children[0].evaluate()[1])
            #print("self.children[1].evaluate(): ", self.children[1].evaluate())
            if self.children[0].evaluate(table):
                self.children[1].evaluate(table)
            else:
                self.children[2].evaluate(table)
    
class Assignment(Node):
    def __init__(self, children):
        super().__init__(None, children)
    
    def evaluate(self, table):
        table.setter(self.children[0].value, self.children[1].evaluate(table))

class FunctionDeclaration(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        
    def evaluate(self, table):
        function_symbol_table.create(self.children[0].value, self)


class FunctionCall(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        
    def evaluate(self, table): 
        node = function_symbol_table.getter(self.value)

        if len(node.children) - 2 != len(self.children):
            raise Exception("Arguments error")

        new_symbol_table = SymbolTable()

        if len(node.children) > 2:
            for i in range(1, len(node.children) - 1): 
                new_symbol_table.create(node.children[i], node.children[i].evaluate(new_symbol_table))
                new_symbol_table.setter(node.children[i].children[0].value, self.children[i-1].evaluate(table))
            return node.children[-1].evaluate(new_symbol_table)
        
        else:
            return node.children[-1].evaluate(new_symbol_table)
      
    
class Return(Node):
    def __init__(self, children):
        super().__init__("return", children)
        
    def evaluate(self, table):
        return self.children[0].evaluate(table)

        
class SymbolTable():
    def __init__(self):
        self.table = {}

    def create(self, key, type):
        if key in self.table:
            raise Exception("variable declaration error")
        elif type == "String":
            self.table[key] = ("String", "")
        elif type == "Int":
            self.table[key] = ("Int", 0)
    
    def setter(self, key, value):
        if key not in self.table:
            raise Exception("undeclared variable")
        if self.table[key][0] != value[0]:
            #print("key in symbol table: ", SymbolTable.table[key][0])
            #print("key in valye: ", value)
            raise Exception("wrong type declaration")
        self.table[key] = value

    def getter(self, key):
        if key not in self.table:
            raise Exception("Symbol not found")
        return self.table[key]

class FunctionTable():
    def __init__(self):
        self.table = {}
    
    def create(self, key, type):
        if key in self.table:
            raise Exception("variable declaration error")
        self.table[key] = type
        
    def setter(self, key, value):
        if key not in self.table:
            raise Exception("undeclared function error")
        if self.table[key] != value[0]:
            raise Exception("variable type error")
        else:
            self.table[key] = value

    def getter(self, key):
        if key not in self.table:
            raise Exception("undeclared function error")
        return self.table[key]        

class Parser():
    #tokenizer = None # objeto da classe que irá ler o código fonte e alimentar o Analisador (Tokenizer)

    @staticmethod
    def parseBlock():
        children = []
        #print('fui chamado')
        while Parser.tokenizer.next.type != 'EOF':
            #print("não sou eof")
            children.append(Parser.parseStatement())
            #print("children")
        return Block(children)
        
    @staticmethod
    def parseStatement():

        current_token = Parser.tokenizer.next

        #print("current token: ", current_token.value, " ", current_token.type)

        if current_token.type == 'ID':
            temp = Identifier(current_token.value) 
            Parser.tokenizer.selectNext()
            current_token = Parser.tokenizer.next

            if current_token.type == 'DECLARE':
                Parser.tokenizer.selectNext()
                current_token = Parser.tokenizer.next

                if current_token.type == 'TYPE':
                    save_type = Parser.tokenizer.next.value
                    Parser.tokenizer.selectNext()
                    current_token = Parser.tokenizer.next

                    if current_token.type == 'EQUALS': # se for para inicializar ja atribuindo valor
                        Parser.tokenizer.selectNext()
                        current_token = Parser.tokenizer.next
                        result = VarDeclaration(save_type, [temp, Parser.parseRelExpression()])
                        current_token = Parser.tokenizer.next

                    else: # se for para inicializar vazia
                        if save_type == "String":
                            result = VarDeclaration(save_type, [temp, StrVal("")])
                        elif save_type == "Int":
                            # print("entrei aquiiii")
                            result = VarDeclaration(save_type, [temp, IntVal(0)])
                    
                    if current_token.type == "ENTER" or current_token.type == "EOF":
                        Parser.tokenizer.selectNext()
                        current_token = Parser.tokenizer.next
                        return result # CHECAR SE NÃO PRECISA DE MAIS UM SELECT NEXT
                    
                else:
                    raise Exception("incorrect declaration of variable")


            if current_token.type == 'EQUALS':
                Parser.tokenizer.selectNext()
                current_token = Parser.tokenizer.next
                result = Assignment([temp, Parser.parseRelExpression()])
                
                current_token = Parser.tokenizer.next
                if current_token.type == "ENTER" or current_token.type == "EOF":
                    #print("buenos dias")
                    Parser.tokenizer.selectNext()
                    current_token = Parser.tokenizer.next
                    return result  # CHECAR SE NÃO PRECISA DE MAIS UM SELECT NEXT
                else: 
                    raise Exception("Varible declaration error")
            #else:
            #    raise Exception("Error of ID")

            if current_token.value =="(":
                
                Parser.tokenizer.selectNext()
                current_token = Parser.tokenizer.next
                function_arguments = []

                while current_token.value != ")":
                    function_arguments.append(Parser.parseRelExpression())
                    current_token = Parser.tokenizer.next
                
                    if current_token.type == "COMMA":
                        Parser.tokenizer.selectNext()
                        current_token = Parser.tokenizer.next
                    else:
                        break

                result = FunctionCall(temp.value, function_arguments)
                
                if current_token.value != ")":
                    raise Exception("Error of closing function call parenthesis")
                
                Parser.tokenizer.selectNext()
                current_token = Parser.tokenizer.next
                
                if current_token.type == "ENTER" or current_token.type == "EOF":
                        Parser.tokenizer.selectNext()
                        current_token = Parser.tokenizer.next
                        
                        return result
            else:
                raise Exception("Variable declaration error")
            
        elif current_token.type == "FUNCTION":
            Parser.tokenizer.selectNext()
            current_token = Parser.tokenizer.next
            
            if current_token.type == "ID": #Lê o nome da função
                function_name = Identifier(current_token.value)
                Parser.tokenizer.selectNext()
                current_token = Parser.tokenizer.next
                
                if current_token.value == "(": # Espera "(" para começar a ler argumentos da função
                    Parser.tokenizer.selectNext()
                    current_token = Parser.tokenizer.next
                    function_arguments = []
                    function_arguments.append(function_name)

                    while current_token.value != ")": # Se a função exigir argumentos:

                        # Argumento declarado dentro da função com tipo das variáveis (ex.: soma(Int :: a = 1, Int :: b = 3)):
                        if current_token.type == "ID":
                            argument_id = Identifier(current_token.value)
                            Parser.tokenizer.selectNext()
                            current_token = Parser.tokenizer.next
                            
                            if current_token.type == "DECLARE":
                                Parser.tokenizer.selectNext()
                                current_token = Parser.tokenizer.next
                                
                                if current_token.type == "TYPE":
                                    argument_type = Parser.tokenizer.next.value
                                    Parser.tokenizer.selectNext()
                                    current_token = Parser.tokenizer.next
                                    if argument_type == "String":
                                        function_arguments.append(VarDeclaration(argument_type, [argument_id, StrVal("")]))
                                    elif argument_type == "Int":
                                        function_arguments.append(VarDeclaration(argument_type, [argument_id, IntVal(0)]))
                                    
                                    if current_token.type == "COMMA":
                                        Parser.tokenizer.selectNext()
                                        current_token = Parser.tokenizer.next
                                        
                                    elif current_token.value == ")":
                                        break
                                        
                                    else:
                                        raise Exception("Function sintax error")                                    
                                else:
                                    raise Exception("Function sintax error")
                            else:
                                raise Exception("Function sintax error")
                        else:
                            raise Exception("Function sintax error")
                        
                    if current_token.value == ")": # Depois de ler os argumentos, começa a ler as operações dentro da função
                        function_children_nodes = []
                        Parser.tokenizer.selectNext()
                        current_token = Parser.tokenizer.next
                        
                        if current_token.type == "DECLARE":
                            Parser.tokenizer.selectNext()
                            current_token = Parser.tokenizer.next
                            
                            if current_token.type == "TYPE":
                                function_type = Parser.tokenizer.next.value
                                Parser.tokenizer.selectNext()
                                current_token = Parser.tokenizer.next
                                
                                if current_token.type == "ENTER":
                                    Parser.tokenizer.selectNext()
                                    current_token = Parser.tokenizer.next
                                    
                                    while current_token.type != "END":
                                        function_children_nodes.append(Parser.parseStatement())
                                        current_token = Parser.tokenizer.next
                                        
                                    function_arguments.append(Block(function_children_nodes))
                                    
                                    if current_token.type == "END":
                                        Parser.tokenizer.selectNext()
                                        current_token = Parser.tokenizer.next
                                        
                                        if current_token.type == "ENTER":
                                            Parser.tokenizer.selectNext()
                                            current_token = Parser.tokenizer.next
                                            
                                            return FunctionDeclaration(function_type, function_arguments)
                                        
                                        else:
                                            #print(Parser.tokenizer.next.value)
                                            raise Exception("Function sintax error")
                                    else:
                                        #print(Parser.tokenizer.next.value)
                                        raise Exception("Function sintax error")
                                else:
                                    #print(Parser.tokenizer.next.value)
                                    raise Exception("Function sintax error")
                            else:
                                raise Exception("Function sintax error")
                        else:
                            raise Exception("Function sintax error")
                    else:
                        raise Exception("Function sintax error")
                else:
                    raise Exception("Function sintax error")
            else:
                raise Exception("Function sintax error")
            
        elif current_token.type == "RETURN":
            Parser.tokenizer.selectNext()
            result = Return([Parser.parseRelExpression()]) 
            current_token = Parser.tokenizer.next
            # print(current_token.type)
            
            if current_token.type == "ENTER" or current_token.type == "EOF":
                Parser.tokenizer.selectNext()
                current_token = Parser.tokenizer.next
                return result
            
            else:
                raise Exception("Return sintax error")
            

        elif current_token.type == 'PRINTLN':
            Parser.tokenizer.selectNext()
            current_token = Parser.tokenizer.next
            if current_token.value == '(':
                #print("oi")
                Parser.tokenizer.selectNext()
                current_token = Parser.tokenizer.next
                result = Parser.parseRelExpression()
                #print("rs", result.value)
                current_token2 = Parser.tokenizer.next
                if current_token2.value == ')':
                    #print("fechou")
                    Parser.tokenizer.selectNext()
                    current_token = Parser.tokenizer.next
                    #print("rs", result.value)
                    result = Println([result])
                    
                    if current_token.type == "ENTER":
                        return result
                    else: 
                        raise Exception("Sintax error")
                else:
                    raise Exception("Error of closing print parenthesis")
            else:
                raise Exception("Error of opening print parenthesis")



        elif current_token.type == "WHILE":
            Parser.tokenizer.selectNext()  # CHECAR SE NÃO PRECISA DE menos UM SELECT NEXT
            cond = Parser.parseRelExpression()
            #print("conddddd    ", cond)
            if Parser.tokenizer.next.type == "ENTER":
                children = []
                #Parser.tokenizer.selectNext()
                while Parser.tokenizer.next.type != "END":
                    children.append(Parser.parseStatement())
                result = While([cond, Block(children)])
                #print('aaaaaaaaaaaaa')
                if Parser.tokenizer.next.type == "END":
                    #print('aaaaaaaaaaaaattt')
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "ENTER":
                        Parser.tokenizer.selectNext()
                        current_token = Parser.tokenizer.next
                        #print("cabou")
                        return result
                        
                    else:
                        raise Exception ("Sintax error")
                return result
            

        elif current_token.type == "IF":
            Parser.tokenizer.selectNext()
            cond = Parser.parseRelExpression()
            #print("condicion", cond)
            if Parser.tokenizer.next.type == "ENTER":
                if_children = []
                Parser.tokenizer.selectNext()
                while Parser.tokenizer.next.type != "END" and Parser.tokenizer.next.type != "ELSE":
                    if_children.append(Parser.parseStatement())
                result = If([cond, Block(if_children)])
                if Parser.tokenizer.next.type == "END":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "ENTER":
                        Parser.tokenizer.selectNext()
                    else:
                        raise Exception ("Sintax error")
                elif Parser.tokenizer.next.type == "ELSE":
                    #print("entrei no else")
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "ENTER":
                        Parser.tokenizer.selectNext()
                        else_children = []
                        
                        while Parser.tokenizer.next.type != "END":
                            else_children.append(Parser.parseStatement())
                        #print("result", result)
                        current_token = Parser.tokenizer.next
                        result = If([result, Block(if_children), Block(else_children)])
                        
                        if Parser.tokenizer.next.type == "END":
                            Parser.tokenizer.selectNext()
                            current_token = Parser.tokenizer.next
                            if Parser.tokenizer.next.type == "ENTER":
                                Parser.tokenizer.selectNext()
                                current_token = Parser.tokenizer.next
                            else:
                                raise Exception ("Sintax error")
                        else:
                            raise Exception ("Sintax error")
                    else:
                        #print(Parser.tokenizer.next.value)
                        raise Exception ("Sintax error")
                else:
                        #print(Parser.tokenizer.next.value)
                        raise Exception ("Sintax error")
            else:
                #print(Parser.tokenizer.next.value)
                raise Exception ("Sintax error")
            
            return result

        elif current_token.type == "ENTER":
            Parser.tokenizer.selectNext()
            current_token = Parser.tokenizer.next
            return NoOp()
        
        else:
            #print(current_token.value)
            raise Exception("Sintax error")
        
    @staticmethod
    def parseRelExpression(): 

        operation_types = ['EQEQUALS', 'GREATER', 'LESS']
        result = Parser.parseExpression()
        current_token = Parser.tokenizer.next

        while current_token.type in operation_types:

            if current_token.type == 'EQEQUALS':
                Parser.tokenizer.selectNext()
                result = BinOp(current_token.value, [result, Parser.parseExpression()])
                current_token = Parser.tokenizer.next 

            elif current_token.type == 'GREATER':
                Parser.tokenizer.selectNext()
                result = BinOp(current_token.value, [result, Parser.parseExpression()])
                current_token = Parser.tokenizer.next

            elif current_token.type == 'LESS':
                Parser.tokenizer.selectNext()
                result = BinOp(current_token.value, [result, Parser.parseExpression()])
                current_token = Parser.tokenizer.next 

        return result
    

    @staticmethod
    def parseExpression(): 

        operation_types = ['PLUS', 'MINUS', 'OR',  'CONCAT']
        result = Parser.parseTerm()
        current_token = Parser.tokenizer.next
        #print("current_token", current_token)

        while current_token.type in operation_types:
            if current_token.type == 'PLUS':
                Parser.tokenizer.selectNext()
                result = BinOp(current_token.value, [result, Parser.parseTerm()])
                current_token = Parser.tokenizer.next 

            elif current_token.type == 'MINUS':
                Parser.tokenizer.selectNext()
                result = BinOp(current_token.value, [result, Parser.parseTerm()])
                current_token = Parser.tokenizer.next 

            elif current_token.type == 'OR':
                Parser.tokenizer.selectNext()
                #print("hallo")
                result = BinOp(current_token.value, [result, Parser.parseTerm()])
                current_token = Parser.tokenizer.next 

            elif current_token.type == 'CONCAT':
                Parser.tokenizer.selectNext()
                result = BinOp(current_token.value, [result, Parser.parseTerm()])
                current_token = Parser.tokenizer.next 
 
        return result

    

    @staticmethod
    def parseTerm():

        operation_types = ['MULT', 'DIV', 'AND']
        result = Parser.parseFactor()
        current_token = Parser.tokenizer.next
        #print("current_token", current_token)

        while current_token.type in operation_types:
            if current_token.type == 'MULT':
                Parser.tokenizer.selectNext()
                # result *= Parser.parseFactor()
                result = BinOp(current_token.value, [result, Parser.parseFactor()])
                current_token = Parser.tokenizer.next  

            elif current_token.type == 'DIV':
                Parser.tokenizer.selectNext()
                result = BinOp(current_token.value, [result, Parser.parseFactor()])
                current_token = Parser.tokenizer.next  
            
            elif current_token.type == 'AND':
                Parser.tokenizer.selectNext()
                result = BinOp(current_token.value, [result, Parser.parseFactor()])
                current_token = Parser.tokenizer.next  

        return result
    

    @staticmethod
    def parseFactor():

        current_token = Parser.tokenizer.next
        if current_token.type == 'INT':
            Parser.tokenizer.selectNext()
            result = IntVal(current_token.value)
            
        elif current_token.type == 'STRING':
            Parser.tokenizer.selectNext()
            result = StrVal(current_token.value)

        elif current_token.value == '(':
            Parser.tokenizer.selectNext()
            result = Parser.parseRelExpression()
            current_token = Parser.tokenizer.next
            #print("aaaa", current_token.value)
            if current_token.value != ')':
                raise Exception('Parenthesis error')
            Parser.tokenizer.selectNext()
            current_token = Parser.tokenizer.next

        elif current_token.type == 'MINUS':
            Parser.tokenizer.selectNext()
            result = UnOp('-', [Parser.parseFactor()])

        elif current_token.type == 'PLUS':
            Parser.tokenizer.selectNext()
            result = UnOp('+', [Parser.parseFactor()])

        elif current_token.type == 'NOT':
            Parser.tokenizer.selectNext()
            result = UnOp('!', [Parser.parseFactor()])

        elif current_token.type == 'ID':
            Parser.tokenizer.selectNext()
            result = Identifier(current_token.value)

            if Parser.tokenizer.next.value == "(":
                Parser.tokenizer.selectNext()
                current_token = Parser.tokenizer.next
                function_arguments = []
                while current_token.value != ")":
                    function_arguments.append(Parser.parseRelExpression())
                    current_token = Parser.tokenizer.next
                    if current_token.type == "COMMA":
                        Parser.tokenizer.selectNext()
                        current_token = Parser.tokenizer.next
                    else:
                        break
                result = FunctionCall(result.value, function_arguments)
                if current_token.value != ")":
                    raise Exception("Parenthesis sintax error")
                Parser.tokenizer.selectNext()
                current_token = Parser.tokenizer.next
                #print(current_token.type)
        
        elif current_token.type == 'READLINE':
            Parser.tokenizer.selectNext()
            current_token = Parser.tokenizer.next
            if current_token.value == '(':
                Parser.tokenizer.selectNext()
                current_token = Parser.tokenizer.next
                if current_token.value != ')':
                    raise Exception('Parenthesis error')
                result = Readln(None)
                Parser.tokenizer.selectNext()
            

        else:
            raise Exception('Order error')
        return result


    @staticmethod
    def run(code):

        filtered_code = PrePro.filter(code)
        #print("filtered code", filtered_code)

        Parser.symbol_table = SymbolTable()
        Parser.function_table = FunctionTable()
        Parser.tokenizer = Tokenizer(filtered_code)
        Parser.tokenizer.selectNext()

        node_zero = Parser.parseBlock()

        result = node_zero.evaluate(Parser.symbol_table)

        if Parser.tokenizer.next.type == 'EOF':
            return result
        else:
            raise Exception('General error')

        


parser = Parser()
function_symbol_table = FunctionTable()
args = sys.argv
with open(args[1], "r") as f:
    string = f.read()
    parser.run(string)