import re

def breakExpr(e):
    if "+" in e:
        left = e.split("+")[0]
        right = "+".join(e.split("+")[1:])
        return breakExpr(left) + breakTerm(right)
    elif "-" in e:
        left = e.split("-")[0]
        right = "-".join(e.split("-")[1:])
        return breakExpr(left) - breakTerm(right)
    else:
        return breakTerm(e)

def breakTerm(e):
    if "*" in e:
        left = e.split("*")[0]
        right = "*".join(e.split("*")[1:])
        return breakTerm(left) * breakFactor(right)
    elif "/" in e:
        left = e.split("/")[0]
        right = "*".join(e.split("/")[1:])
        return breakTerm(left) / breakFactor(right)
    else:
        return breakFactor(e)

def breakFactor(e):
    if re.match("^\d+$",e):
        return int(e)
    else:
        print("I have no idea what ur on with this '%s' bullshit"%e)
        exit(1)


myExpr = "5*2-5/10+8"
print(breakExpr(myExpr))
