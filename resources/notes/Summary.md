## PAST PAPER TIPS
---

When doing leftmost derivation, structure like this

sentence ⇒lm fnc

and just stop at id don't give the lexme (sometimes)

follow sets don't have epsilon in them, either you are follwoed by EOF or a token obviously. 

LL(1) parsing tables also do not have epsilon but do have end of file!

remember functions have highest scope. 

remember unless a experssion is empty, a assign expression, or a void call, it will have a value on the stack. 


## QUESTIONS
---

1. Whats up with Chomsky’s Hierarchy????

not in the exam

2. do we need to memorise JVM instructions?

no need to memorise, there is appendix. 

3. define regular grammar/expression

all transformations must be A->aB

4. might be a good idea to memorise the exact algorithm of subset constuction + DFA minimisation :/

5. L and S

L is inheritend information from a left to right pass
S is synthesised information in which we only need to look at our children. 

6. revise follow set algorithm
all G

7. note that left recursion enforces left assoiativity and right right

8. if two nodes have equal precendence then assoicativity groups elements

9. the higher in the tree the lower the precedence. 

## EXAM PLAN
---

1. revise lectures
2. do past papers + read over this
3. revise assignment code + tutorial questions


## Intro
---

The only part of the compiler that needs to know the arcitecture of the machine it's compiling for is the Code generation step. 

retargetable compilers run off the idea that multiple different languages can be compiled into the same IR using multiple front ends. Once in this form you can use generic IR optimization tools and then feed this ir into different back ends depending on the system. 

M languages + N architectures -> M frontends + N backends

not MN frontends + NN backends

## Lexical Analysis
---

Tokens are just a basic unit of syntax, a token in the enlish language is a word for example. 

a lexeme is the actual text forming a token, known to be a `instance` of a token. 

Note tokens can also have attributes which basically just describe the tokens value for later steps. 

Tokenisation is done by the lexer usually through regex or other patterns. 
Note that if a token begings to get matched but doesn't get fully matched (like a string with no terminating double quote) this can be raised as a lexical error. 

some lexical errors stop the compiler because they are unrecoverable (like a open comment with no close) whereas other's can be recovered from by going to the next white space / new line. 

note the only difference between Kleene Closure and Positive closure is that postive closure can't have the empty string. Note that L^3 is a klene closure with a set limit, as in L* but rather then ANY amount of L we only have no L, one L, LL, or LLL. 

remember that a Language is a set of Strings in a certain alphabet. further note with RE * has the highest precendence followed by concatentation and "|". Stating this lets us take out brackets. 

A|B*C is the same as (A)|(B\*C) NOT (A|B)\*C as the \* attaches to the B first, then the C attaches to the B\* and that whole stement attaches to the A via |

a Finate State Automata is in essence just a way to represent a machine/automata/system which has a finite number of states and a fixed set of ways to transition between those state. for ys it lets us define symbols in a alphabet and how you can transition from one to another. 

in a DFA every input causes a state change. You can convert RE into NFA's through a series of ways, One of those ways is Thompsons construction. This method is syntax driven, Inductive, and important.

Inductive just means the cases in the construction of the NFA follow the cases in the definition of REs and important means that if a symbol occurs several times in a RE , a separate NFA is constructed for each occurrence

## Syntax analysis
---

this is the parser, it groups tokens together into gramatical phrases. YOu can do this in many ways but representing this grouping as a AST is quite effective and common. 

Because the pardsr works off a grammar it can correct errors and give meaningful error messahes about how the statement was structured rather then why it doesn't translate into machine code. 

this thens feeds into the symantic analyser (the recogniser) which does type checking and makes sure the ast is valid given the language constraints. 

For programming languages semantics can be split into two parts

Static Semantics is context-sensitive restrictions enforced at compile-time stuff like all identifiers declared before use, assignment must be type-compatible etc. 

Run Time Semantics is what the program does or computes, i.e the meaning of a program or what happens when it is executed. Is specified by code generation routines.

syntax-directed translation is where a grammar is defined in a way that we can skip every step after the parser and go straight to code generation. 

note that context free grammars and context sensitive grammars are different because in a context free grammar the left side must be a single non terminal. 
I.e the non terminal evalutes to the same set of terminals and non terminals regardless of context. Whereas for a context sensitive grammar we can have `aAbB -> aabb` where the non terminals in the left have a context of other non terminals and terminals surronding them. 

note sentential forms are the transition states of a sentence as it ets converted from grammar to concrete. i.e
```
<sentence>
<word> SPACE <word>   (this is a sentential form)
HELLO SPACE WORLD
```

a CFL (context free language) is the language generated by a CFG. remember the CFG specifies a set of strings over some alphabet, this set of strings forms a language. 

why do we use a tree rather then a left/right derrivation??It's a graphical representation of the same information and makes it easier to think, furthermore computer science is deeply familiar with tree structures and has gotten very good at manipulating them.

note that a BNF is the pure form of CFG and EBND has regex in it with the ? and + and *.

note, higher precedence operators bind to their operands before lower precedence operators and thus appear lower in the tree.
`A + B * 10` breaks down to `A+(B*10)` because `*` has higher precendence. 

note a grammar is ambigious if the same sentence can be interpreted in more then one way.

note Regular Expressions and Regular Grammars both define a set of strings over some alphabet and are basically the same. The expressions are usually just expressed differently. Note that Finite Automata also do the same thing, define a set of strings over a alphabet. 
All three define a language. 
But note all 3 can't "count" or "nest" meaning that you can't enforce decleration before use of a indeifier unless you enforce that all variables must be in a block before the code starts. (which is what VC does lmao)
Furthermore it can't count/check types with a declaraton so it really can't do function param checking or type checking. 

a right linear grammar is one with at most 1 non-terminal on the right end of the result side. `A->aB`

when converting right linear grammars to NFA's remember to have only 1 end state as the structure basically enforces that you add in a new non terminal state that translates to epsilon. You can't have a non terminal convert to a terminal because then it isn't right linear!!!

the first set for a non terminal is the left most non terminal that arsies if you keep reducing the left hand side as much as possible. Note that you only add in epsilon into the first set if the entire symbol can evaulate to epsilon, not if one of the non terminals involved goes to epsilon. 

The expression Grammar is a form of grammar that does not have any left recursion and thus no ambiguity. With left recursion we don't know how many times we will loop for. 

Follow sets tell us the series of symbols that follow a given nonterminal A which helps us determine if removing this non terminal is the right move. 
take this example

S -> aAb
A -> a | <epsilon>
consider parsing the string 'ab' we go S->aAb then A->epsilon

when we have aAb our logic would go "alright we have a, the lookahead symbol is now b, how can we convert A into b" and would crash. BUT if we said "alright well Follow(A) = {b} lets just have A go to epsilon to get our lookahead token in a round about way"

The select set for a production A→α:

If epsilon is in First(α), then
    Select(A→α) = (First(α) − {ϵ}) ∪ Follow(A)
Otherwise:
    Select(A→α) = First(ϵϵ)

A grammer is LL(1) is for every nonterminal the select set of every branch produces a unique terminal. i.e no two branches can ever produce the same terminal. Once we have this we know there is only one specific path that leads to null because null can only appear once by the rules. This means we don't have to worry about null in any of the parsing, hence select sets just becomes first sets other then the single nullable case!

Note that Left Recursion means that we can't be LL(1) because we can go into a infinite loop if we try to follow the left most path. Non-Direct Left Recursion is just something like A->Ba B->Ab. 

Note that if you have statements with common prefixes then you can't have LL(1) cause you need another lookahead token to tell which of the two to choose. see dangling else grammar. 

A Table-driven Ll(1) parser can't handle left recursion cause then you have 2 entries in 1 cell. 1 for the terminating step and one for the recurrsive case. also remember with table driven that $ is a valid terminal. 

note LL(1) parsers can count / balance parenthesis. think about S->(S)|epsilon
the table will look like
```
  | (  | ) | $
---------------
S | (S)| e | e
```

if we parse `(())` we are fine but try to do `(()` and it fails on scanning the `)`. This is because the table driven parser uses a stack!

note that a preducated LL(k) uses a conditional to help chose between two conflicting productions at runtime of a parser generator. 

A phrase of a grammar G is a string of terminals labelling the terminal nodes (from left to right) of a parse tree

note the AST takes out a lot of stuff like the key words and brackets and stuff as it's all only there to help build the tree. afterwards it's useless. 

An attribute grammar is just a CFG with a set of transformation to give each grammar to give each non terminal a attribute or set of attributes. 

Semantic analysis is the context sensitive analysis step and enforces thigs that a CFG can't, such as all variables must be defined before used. An attribute grammar lets us enforce context sensitive constraints. 

Synthesised attributes computed from children Inherited attributes computed from parent and siblings

a decorated parse tree is just a parse tree with added attribute grammar elements. 

You can evalute an attribute grammar (fill in the values of the attributes for each node) by walking the tree although this assumes that the attribute grammar is non circular (no attribute depends on itself) and finding if a grammar is circular or not takes exponential time to figure out. 

We can also do this via Rule based methods, where a programmar hardcodes a evaluation order at compiler-construction time. 

An L attributed Grammar is one where you can traverse the decorated parse tree left to right in 1 pass and have all the attributes filled in. An attribute grammar is L-attributed if the inherited symbols on the right hand side of every non-terminal transformation depend only on the attributes of symbols to the left of the symbol and the inherited attributes of the symbol. The L comes from the information flowing from left to right.

An attribute grammar is S-attributed if it uses synthesised attributes only. These grammars allow for parsing and semantic analysis in one pass in bottom-up parsers.The information always flows up in the tree as all attributes are synthesised and don't need any information from higher in the tree to be derrived.

Every S-attributed grammar is L-attributed. This is because if there are no inherited attributes there is nothing that MUST be evaluated before contining a traversal. So we can happily progress left to right.

Think about it, a L attributed grammar only uses inherited attributes and the syntehsised attributes of non terminals on it's left. That is to say that as you go through a transformation left to right you never need to look further to the right to give the current non terminal a attribute. An S attributed grammar is the same but doesn't need the inherited attributes simply relying on the synthesised attributes of the non terminals to the left of any non terminal. 

A Block structured language permits the nesting of blocks, note though that c is not strictly block-structured because you can't nest functions inside of functions 

Most closed nested rule: for multiple defintions grab the one in the cloest scope. 



## Immediate code generation
---

The Intermediate Code Generator generates an explicit IR from the AST. The IR isn't like universally defined but it must be easy to generate while also being easy to convert into machine code.

for some compilers this step can be skipped and the AST is used to generate code directly. (what we do with our decorated AST)

note some common optimisations that can we done on the IR is to remove code that can't be reached, replace some variable access with a constant if it happens a lot and remove reduant computation or move code around so it runs better. 

• invokevirtual: on the dynamic type of objref `strInstance.count()`
• invokestatic: based on the static class of objref `String.format()`

invokespecial // also known as invokenonvirtual
    - the instance initialisation method <init>
    - a private method of "this"
    - a method in a super class of "this"
    - invokespecial is used to call methods without concern for dynamic binding, in order to invoke the particular class’ version of a mehod.

