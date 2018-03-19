class Node():
    def __init__(self, name, transitions, terminal):
        self.name = name
        self.transitions = transitions
        self.terminal = terminal

s = Node("START",[],False)

# a+b|c
A = Node("A",[],False)
A.transitions.append(("a",A))

B = Node("B",[],True)
C = Node("C",[],True)
s.transitions.append(("a",A))
A.transitions.append(("b",B))
A.transitions.append(("c",C))

def match(dfa, check):
    curr = dfa
    check = list(check)
    i = 0
    while not (curr.terminal and i == len(check)):
        if i == len(check):
            return False
        seen = False
        for trans in curr.transitions:
            if trans[0] == check[i]:
                i+=1
                curr = trans[1]
                seen = True
                break
        if not seen:
            return False
    return True



print("Give me da string")
string = input("> ")
if match(s,string):
    print("Match!")
else:
    print("Invalid.")
