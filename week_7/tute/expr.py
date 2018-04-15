# ⟨S⟩ → ⟨expr⟩
# ⟨expr⟩ → ⟨expr⟩ / ⟨expr⟩
# ⟨expr⟩ → num
# ⟨expr⟩ → num . num

class Token():
    def __init__(self, type, lexme, float):
        self.type = type
        self.lexme = lexme
        self.float = float
    def isFloat(self):
        return self.float
    def show(self):
        return self.lexme

class binaryExpr():
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def show(self):
        return "("+self.left.show()+" "+self.op.lexme+" "+self.right.show()+")<%s>"%self.isFloat()
    def isFloat(self):
        return self.left.isFloat() or self.right.isFloat()

# i'm just gonna build the tree manually cause i'm lazy
# 1.0/1.8/2/1
l = Token("NUM","1.0",True)
o = Token("DIVIDE","/",False)
r = Token("NUM","1.8",True)
le = binaryExpr(l,o,r)
l2 = Token("NUM","2",False)
o2 = Token("DIVIDE","/",False)
r2 = Token("NUM","1",False)
re = binaryExpr(l2,o2,r2)
o3 = Token("DIVIDE","/",False)
e = binaryExpr(le,o3,re)
print(e.show())
