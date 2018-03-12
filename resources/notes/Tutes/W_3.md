# Tute 1

tutor: cjdb.ns@gmail.com

make the subject: COMP3131 -- (subject)

## Regular expressions
---

a) `(0|1)*`
b) `()` or $\phi$
c) $\epsilon$
d) `011`
e) `0|011` or `0(11)?`
f) `1(0|1)*`
g) `1(0|1)*0` 
h) `0*10*10*10*`
i) `1(1|01)*`

## DFA
---

take note of the end states, you can end in multiple places validly. 

## NFA
---

the 3 states a regex can be in is closure (*) alternation (A|b) or concatenation (ab)

## Coding
---

1. `egrep ^y(.*y)?$`
