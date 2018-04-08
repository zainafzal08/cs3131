table = {
    "|": {"E":None,"P":"|TP","T":None,"Q":"e","F":"e","R":"e"},
    "(": {"E":"TP","P":None,"T":"FQ","Q":"FQ","F":"(E)R","R":"e"},
    ")": {"E":None,"P":"e","T":None,"Q":"e","F":None,"R":"e"},
    "i": {"E":"TP","P":None,"T":"FQ","Q":"FQ","F":"iR","R":"e"},
    "*": {"E":None,"P":None,"T":None,"Q":None,"F":None,"R":"*R"},
    "$":{"E":None,"P":"e","T":None,"Q":"e","F":None,"R":"e"}
}

def isTerminal(s):
    if s in table.keys():
        return True
    return False


inp = "(i|i)*$"
stack = []
stack.append("$")
stack.append("E")

i = 0
token = inp[i]

# print state
print("Stack: %s"%str(stack))
print("Input: %s"%inp)
input(".")

while len(stack) > 0:
    curr = stack.pop()
    if isTerminal(curr):
        if curr != token:
            raise Exception("FUCK")
        else:
            i+=1
            token = inp[i]
    else:
        for c in reversed(list(table[token][curr])):
            if c != "e":
                stack.append(c)

    # print state
    print("Stack: %s"%str(stack))
    print("Input: %s"%inp[i:])
    input(".")
