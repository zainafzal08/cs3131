import re

def breakExpr(e):
    if "+" in e:
        left = e.split("+")[0]
        right = e.split("+")[1]
        return "(%s+(%s))"%(breakExpr(left),breakTerm(right))
    elif "-" in e:
        left = e.split("-")[0]
        right = e.split("-")[1]
        return "(%s-(%s))"%(breakExpr(left),breakTerm(right))
    else:
        return breakTerm(e)

def breakTerm(e):
    if "*" in e:
        left = e.split("*")[0]
        right = e.split("*")[1]
        return "(%s*(%s))"%(breakTerm(left),breakFactor(right))
    elif "/" in e:
        left = e.split("/")[0]
        right = e.split("/")[1]
        return "(%s/(%s))"%(breakTerm(left),breakFactor(right))
    else:
        return breakFactor(e)

def breakFactor(e):
    # only x is allowed as a ID lol
    if e == "x":
        return "x"
    elif re.match("\d+",e):
        return e
    else:
        return "(%s)"%breakExpr(e)

myExpr = "5*2-5/10+8"
print(breakExpr(myExpr))
