# E -> TQ
# Q -> +TQ | -TQ | e
# T -> FR
# R -> *FR | /FR | e
# F -> INT | (E)

class Token():
    def __init__(self, lex, type):
        self.lex = lex
        self.type = type

class Node():
    def __init__(self, name):
        self.name = name
        self.token = None
        self.children = []
        self.parent = None
    def show(self, i,j):
        print(" "*i+":%s"%self.name)
        for c in self.children:
            c.show(i+j,j)
    def evaluate(self):
        #print("@ %s"%self.name)
        if self.token:
            try:
                return int(self.token.lex)
            except:
                return None
        if self.name == "ROOT":
            return self.children[0].evaluate()
        elif self.name == "E":
            t = self.children[0]
            q = self.children[1]
            if len(q.children) == 0:
                return t.evaluate()
            elif q.children[0].name == "PLUS":
                return t.evaluate() + q.evaluate()
            elif q.children[0].name == "MINUS":
                return t.evaluate() - q.evaluate()
        elif self.name == "Q":
            t = self.children[1]
            q = self.children[2]
            if len(q.children) == 0:
                return t.evaluate()
            elif q.children[0].name == "PLUS":
                return t.evaluate() + q.evaluate()
            elif q.children[0].name == "MINUS":
                return t.evaluate() - q.evaluate()
        elif self.name == "T":
            f = self.children[0]
            r = self.children[1]
            if len(r.children) == 0:
                return f.evaluate()
            elif r.children[0].name == "DIVIDE":
                return f.evaluate() / r.evaluate()
            elif r.children[0].name == "MULTIPLY":
                return f.evaluate() * r.evaluate()
        elif self.name == "R":
            f = self.children[1]
            r = self.children[2]
            if len(r.children) == 0:
                return f.evaluate()
            elif r.children[0].name == "DIVIDE":
                return f.evaluate() / r.evaluate()
            elif r.children[0].name == "MULTIPLY":
                return f.evaluate() * r.evaluate()
        elif self.name == "F":
            if len(self.children) == 1:
                return self.children[0].evaluate()
            return self.children[1].evaluate()
        return None
class Scanner():
    def __init__(self, r):
        self.tokens = []
        self.curr = ""
        self.debug = False
        self.i = 0
        self.done = False
        self.currType = None
        self.types = {
            "+" : "PLUS",
            "-" : "MINUS",
            "*" : "MULTIPLY",
            "/" : "DIVIDE",
            "(" : "LPAREN",
            ")" : "RPAREN"
        }
        for c in r:
            if c.isdigit():
                self.curr += c
                self.currType = "NUM"
            elif self.isValidChar(c):
                if self.currType != None:
                    self.appendToken()
                self.curr += c
                self.currType = self.types[c]
                self.appendToken()
            else:
                raise Exception("The fuck is this: %s"%c)
        if self.currType != None:
            self.appendToken()
        self.tokens.append(Token("$","EOF"))

    def isValidChar(self, c):
        if c == "+" or c == "-":
            return True
        elif c == "/" or c == "*":
            return True
        elif c == "(" or c == ")":
            return True
        return False

    def appendToken(self):
        self.tokens.append(Token(self.curr,self.currType))
        self.curr = ""
        self.currType = None

    def peek(self):
        if self.done:
            return None
        return self.tokens[self.i]

    def next(self):
        if self.done:
            return None
        if self.debug:
            print("ACCEPTING %s"%self.peek().type)
        self.i+=1
        if self.i >= len(self.tokens):
            self.done = True
        return self.tokens[self.i-1]

class Parser():
    def __init__(self, s):
        self.scanner = s
        self.root = Node("ROOT")
        self.currNode = self.root

    def accept(self, exp):
        t = self.scanner.next()
        if t.type != exp:
            raise Exception("Unexpected Token of Type %s"%lh.type)
        new = Node(t.type)
        new.token = t
        self.currNode.children.append(new)

    def decend(self,n):
        new = Node(n)
        new.parent = self.currNode
        self.currNode.children.append(new)
        self.currNode = new

    def ascend(self):
        self.currNode = self.currNode.parent

    def generateTree(self):
        self.parseE()
        #self.root.show(0,2)
        return self.root
    
    def parseE(self):
        self.decend("E")
        self.parseT()
        self.parseQ()
        self.ascend()
    
    def parseQ(self):
        self.decend("Q")
        lh = self.scanner.peek()
        if lh.type == "PLUS" or lh.type == "MINUS":
            self.accept(lh.type)
            self.parseT()
            self.parseQ()
        self.ascend()
    
    def parseT(self):
        self.decend("T")
        self.parseF()
        self.parseR()
        self.ascend()

    def parseR(self):
        self.decend("R")
        lh = self.scanner.peek()
        if lh.type == "DIVIDE" or lh.type == "MULTIPLY":
            self.accept(lh.type)
            self.parseF()
            self.parseR()
        self.ascend()

    def parseF(self):
        self.decend("F")
        lh = self.scanner.peek()
        if lh.type == "NUM":
            self.accept("NUM")
            self.ascend()
            return
        elif lh.type == "LPAREN":
            self.accept("LPAREN")
            self.parseE()
            self.accept("RPAREN")
            self.ascend()
            return
        elif lh.type == "EOF":
            self.ascend()
            return
        raise Exception("Unexpected Token of Type %s"%lh.type)


while True:
    i = input("> ")
    s = Scanner(i)
    p = Parser(s)
    tree = p.generateTree()
    print(">> %d"%tree.evaluate())
