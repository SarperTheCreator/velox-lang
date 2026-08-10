import re

# ==================================================
# 1. TOKEN TİPLERİ VE LEXER (Jetonlaştırıcı)
# ==================================================
TOKEN_TYPES = [
    ('STRING',   r'"[^"]*"'),               # Çift tırnak içi metinler ("metin")
    ('NUMBER',   r'\d+'),                   # Tam sayılar
    ('EQ',       r'=='),                    # Eşit mi?
    ('NEQ',      r'!='),                    # Eşit değil mi?
    ('ASSIGN',   r'='),                     # Atama
    ('LT',       r'<'),                     # Küçük mü?
    ('GT',       r'>'),                     # Büyük mü?
    ('PLUS',     r'\+'),                    # Artı (Sayı toplama veya String birleştirme)
    ('MINUS',    r'-'),                     # Eksi
    ('MUL',      r'\*'),                    # Çarpı
    ('DIV',      r'/'),                     # Bölü
    ('LPAREN',   r'\('),                    # Sol parantez
    ('RPAREN',   r'\)'),                    # Sağ parantez
    ('LBRACE',   r'\{'),                    # Sol süslü {
    ('RBRACE',   r'\}'),                    # Sağ süslü }
    ('KEYWORD',  r'\b(deger|yaz|eger|yoksa)\b'), # Anahtar kelimeler
    ('IDENT',    r'[a-zA-Z_]\w*'),          # Değişken isimleri
    ('SKIP',     r'[ \t\n]+'),              # Boşluklar
    ('MISMATCH', r'.'),                     # Tanımsız karakter
]

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

def lexer(code):
    tokens = []
    regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES)
    
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()
        
        if kind == 'STRING':
            # Tırnak işaretlerini soyup temiz metni alıyoruz
            tokens.append(Token('STRING', value[1:-1]))
        elif kind == 'NUMBER':
            tokens.append(Token('NUMBER', int(value)))
        elif kind == 'KEYWORD':
            tokens.append(Token('KEYWORD', value))
        elif kind == 'IDENT':
            tokens.append(Token('IDENT', value))
        elif kind in ('EQ', 'NEQ', 'ASSIGN', 'LT', 'GT', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE'):
            tokens.append(Token(kind, value))
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Tanımsız Karakter: '{value}'")
            
    tokens.append(Token('EOF', None))
    return tokens


# ==================================================
# 2. AST (SOYUT SÖZDİZİMİ AĞACI) DÜĞÜMLERİ
# ==================================================
class NumberNode:
    def __init__(self, value):
        self.value = value

class StringNode:
    def __init__(self, value):
        self.value = value

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class VarAssignNode:
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

class VarAccessNode:
    def __init__(self, var_name):
        self.var_name = var_name

class PrintNode:
    def __init__(self, expr):
        self.expr = expr

class IfNode:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class BlockNode:
    def __init__(self, statements):
        self.statements = statements


# ==================================================
# 3. PARSER (Jetonları Ağaca Dönüştürücü)
# ==================================================
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token().type == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Beklenen Token: {token_type}, Bulunan: {self.current_token().type}")

    def factor(self):
        token = self.current_token()
        
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return NumberNode(token.value)
            
        elif token.type == 'STRING':
            self.eat('STRING')
            return StringNode(token.value)
            
        elif token.type == 'IDENT':
            self.eat('IDENT')
            return VarAccessNode(token.value)
            
        elif token.type == 'KEYWORD' and token.value == 'yaz':
            self.eat('KEYWORD')
            self.eat('LPAREN')
            expr = self.expr()
            self.eat('RPAREN')
            return PrintNode(expr)
            
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
            
        raise SyntaxError(f"Geçersiz Sözdizimi: {token}")

    def term(self):
        node = self.factor()
        while self.current_token().type in ('MUL', 'DIV'):
            token = self.current_token()
            self.eat(token.type)
            node = BinOpNode(node, token.value, self.factor())
        return node

    def arith_expr(self):
        node = self.term()
        while self.current_token().type in ('PLUS', 'MINUS'):
            token = self.current_token()
            self.eat(token.type)
            node = BinOpNode(node, token.value, self.term())
        return node

    def comp_expr(self):
        node = self.arith_expr()
        if self.current_token().type in ('EQ', 'NEQ', 'LT', 'GT'):
            token = self.current_token()
            self.eat(token.type)
            node = BinOpNode(node, token.value, self.arith_expr())
        return node

    def block(self):
        self.eat('LBRACE')
        statements = []
        while self.current_token().type != 'RBRACE' and self.current_token().type != 'EOF':
            statements.append(self.expr())
        self.eat('RBRACE')
        return BlockNode(statements)

    def expr(self):
        token = self.current_token()
        
        if token.type == 'KEYWORD' and token.value == 'deger':
            self.eat('KEYWORD')
            var_name = self.current_token().value
            self.eat('IDENT')
            self.eat('ASSIGN')
            expr_node = self.expr()
            return VarAssignNode(var_name, expr_node)

        elif token.type == 'KEYWORD' and token.value == 'eger':
            self.eat('KEYWORD')
            self.eat('LPAREN')
            condition = self.expr()
            self.eat('RPAREN')
            then_branch = self.block()
            
            else_branch = None
            if self.current_token().type == 'KEYWORD' and self.current_token().value == 'yoksa':
                self.eat('KEYWORD')
                else_branch = self.block()
                
            return IfNode(condition, then_branch, else_branch)

        return self.comp_expr()

    def parse(self):
        return self.expr()


# ==================================================
# 4. EVALUATOR (Çalıştırıcı)
# ==================================================
class Interpreter:
    def __init__(self):
        self.variables = {}

    def visit(self, node):
        if isinstance(node, NumberNode):
            return node.value

        elif isinstance(node, StringNode):
            return node.value

        elif isinstance(node, BinOpNode):
            left = self.visit(node.left)
            right = self.visit(node.right)

            if node.op == '+':
                # Eğer taraflardan biri String ise metin birleştirme yap
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            elif node.op == '-': return left - right
            elif node.op == '*': return left * right
            elif node.op == '/': return left / right
            elif node.op == '==': return 1 if left == right else 0
            elif node.op == '!=': return 1 if left != right else 0
            elif node.op == '<':  return 1 if left < right else 0
            elif node.op == '>':  return 1 if left > right else 0

        elif isinstance(node, VarAssignNode):
            val = self.visit(node.expr)
            self.variables[node.var_name] = val
            return val

        elif isinstance(node, VarAccessNode):
            if node.var_name in self.variables:
                return self.variables[node.var_name]
            raise NameError(f"Tanımsız Değişken: '{node.var_name}'")

        elif isinstance(node, PrintNode):
            val = self.visit(node.expr)
            print(val)
            return val

        elif isinstance(node, BlockNode):
            last_val = None
            for stmt in node.statements:
                last_val = self.visit(stmt)
            return last_val

        elif isinstance(node, IfNode):
            condition_val = self.visit(node.condition)
            if condition_val != 0:
                return self.visit(node.then_branch)
            elif node.else_branch is not None:
                return self.visit(node.else_branch)
            return None

        raise Exception(f"Bilinmeyen Düğüm Tipi: {type(node)}")


# ==================================================
# 5. CANLI TERMINAL (REPL)
# ==================================================
def run_repl():
    interpreter = Interpreter()
    print("=" * 45)
    print(" ⚡ VELOX-LANG v1.2 (String & Metin Destekli) ⚡")
    print(" Çıkmak için 'cikis' yazın.")
    print("=" * 45)

    while True:
        try:
            code = input("velox > ")
            if code.strip() == "cikis":
                break
            if not code.strip():
                continue

            tokens = lexer(code)
            parser = Parser(tokens)
            ast = parser.parse()
            result = interpreter.visit(ast)
            
            if result is not None and not isinstance(ast, (VarAssignNode, PrintNode, IfNode)):
                print(result)

        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    run_repl()