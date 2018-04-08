# E -> TQ
# Q -> +TQ | -TQ | e
# T -> FR
# R -> *FR | /FR | e
# F -> INT | (E)

class Token():
    def __init__(self, lex, type):
        self.lex = lex
        self.type = type

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

class Recogniser():
    def __init__(self, s):
        self.scanner = s
    def doTheThing(self):
        self.parseE()

    def parseE(self):

    def parseQ(self):

    def parseT(self):

    def parseR(self):

    def parseF(self):


s = Scanner("508-8*9-6")
s.debug = True
r = Recogniser(s)
r.doTheThing()
print("Valid!")
