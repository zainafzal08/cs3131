# Static Semantics

## Intro
---

Static semantics is broadly any requirements imposed at compile time for the program to be considered "good" or "well formed". Stuff like "variables have to be defined before they are used" is static semantics. This is stuff we can't enforce with a CFG and thus we need to have the step of semantic analysation via a semantic analyser.

The semantic analyser enforces a languages semantic constraints. there are two types of constraints

1. Scope Rules
2. Type Rules

And the semantic analysis happens in 2 phases
1. Identification (symbol table)
2. Type checking

All stuff we have dealt with before in programming.
Our assignment 4 uses 1 pass to do both these steps and esstentially is a type checker.

## Blocks
---

A Block is a language construct that can contain declerations for example

- the compilation units (code files)
- Procedures and functions and methods
- compound statements

It's basically just any section of code that has a distinct scope.

Within VC we have 2 block types

1. the entire program (i.e the outermost block)
2. compound statements, anything within curly braces `{ ... }`

> A Block structured language permits the nesting of blocks, note though that c is not strictly block-structured because you can't nest functions inside of functions

## Scope
---

We know what the scope of a decleration or variable is, what's new is the idea of scope rules which provide info on what decleration every variable is referring to.

#### Scope Rules in VC

1. the scope of a function is from the point it is declared to the end of the file
2. the scope of a variable in a block is from the point it is declared to the end of the block
3. the scope of a `formal parameter` is the same as the local variable in the function body. i.e function paramaters
4. The scope of a built-in function is the entire program.
5. no identifier can be declared more then once in a block
6. Most closed nested rule: For every use of an identifer I in a block B there must be a corresponding decleration, in block B which is in the smallest enclosing block that contains any declaration of I
7. Due to rule 6 if we have a block inside of a block we have a `scope hole` where if the same identifier is declared twice the inner decleration hides the upper one and the outer decleration is not visible in the innter decleration

consider this

```c
int k;
void foo() {
    int i;
    int j;
    i = 1;
    j = 7;
    putIntLn(i); //1
    putIntLn(j); //7
    {
        // this i overrides the previous i
        // and is invisible to the upper scope.
        int i;
        i = 2;
        putIntLn(i); // 2
        // the j has no decleration here
        // so the one in the above scope is grabbed
        // as if it was global!
        putIntLn(j); // 7
    }
    // the i within the scope hole basically
    // never existed
    putIntLn(i); //1
    putIntLn(j); //7
}
```

So with scope rules we basically can give every decleration a level.

The declerations in the outermost block are level 1 and as we nest deeper we get into higher levels. Typically the pre-defined functions variables and constants are in level 0 or 1.

Within VC we enforce that all functions and global variables are in level 1 and all built in functions are in level 1 (i.e they cannot be redeclerated as user functions or global variables, the user can not have a function called prtinf)


## Identification
---

#### Intro

Identification is the process by which we relate each applied occurance of an identifier to it's decleration and report an error if no such decleration exists.

A symbol table helps us do type checking by associating identifiers with their attributes. The attributes just being the variables type or the functions result type / type of input paramaters. The decleration types basically.

We can represent attributes in 2 ways, either we put the information from the decleration into the table (common) or we have a pointer to the declaration object itself (we do this in assignment 4).

#### VC

How we do this in assignment 4 is via the inherited attribute `decl`  of type `AST` within each symbol class.

We then have two classes, the SymbolTable which holds a set of IdEntrys.

- IdEntry
    - id : the lexeme
    - level : the scope level
    - attr : pointer to the corresponding decleration in the AST
- SymbolTable
    - constructor: creates a new table, set current scope level to 1
    - insert :  isert a new id entry into the table, called at decleration
    - retrieve : gets the entry for an id, is called at each applied occurance of an id
    - retrieveOneLevel : same as retrieve but set to the current scope level
    - openScope: decend down into a deeper scope level
    - closeScop: ascend up a scope level

#### Tasks in Identification

There are two tasks in identification

1. Processing declerations
    - Calling openScope and closeScope when needed
    - Call insert when needed
2. Processing applied occurences
    - decorating ident nodes
    - calling retrieve to link the field Decl in an Ident node to it's decleration in the symbol table
    - Decl = null if no corresponding decleration found, this can then be used to report errors

#### Standard Enviornment

note that at the start of identfication the symbol table contains 11 small ASTs for the nine built in functions such as getInt, putInt, putIntLn etc. and some more spots for primitive types.

These collectively form the standard enviornment and usually are set up by a function such as `establishStdEnvironment()` in the checker

#### Industry

although we are using on symbol table as a stack of all scopes this isn't how it's done in industry stregnth compilers. There we get a new symbol table for each scope and the tables are linked from inner to outer.

Furthermore more efficient data structures for tables are used such as Hash tables and BInary search trees.

they also have the need to handle languages that import and export scopes. (think about java)

## Type Checking
---

So we have a thing called a `Data Type` which is a set of values plus a set of operations on the values. In this way we have data types of strings and numbers and boolean values.

Now as we do these operations we have to make sure that it's valud. I.e expressions are well typed using the type rules, the flow of control works (breaks only within loops) and that things that must be unique are (the labels in a switch statement for example)

So `Type Rules` are the rules to infer the type of each language construct and decide whether the construct has a valid type.

Type Checking is thus just applying the languages type rules to infer the type of each construct and making sure that it's expected.

#### VC

VC is statically type checked (type isn't decided dynamically like python) it has a set of checks that are done under type checking.  for example expressions must have an operator applied to compatible operands, i.e you can't `+` two booleans together. It also has a full set of type rules defined in the spec.

How we can do type checking within ass4 for expressions is by checking the expressions symbols "type" attribute which all concrete expr classes inherit.

if at any point types arn't what they need to be the type is set to error and is handled at the top.

note that type is now an attribute in simple variables as well.

#### Bottom-Up Computation of type in an Expression AST

For a Literal it's type is known from the moment it is tokenised.

for a identifier it's type is obtained from the inheriteded attribute Decl associated with every Ident node

Now for a binary operation such as $E_{1} O E_{2}$ where O is a binary operator of type $T_{1} \times T_{2} \rightarrow T_{3}$ the type checker ensures that $E_{1}$ is of type $T_{1}$ etc. and thus we can infer if all the types match that the result will be of type $T_{3}$

#### Standard Enviornment Class

StdEnvironment is a class with the five static variables:

```java
StdEnvironment.intType = new IntType(dummyPos);
StdEnvironment.floatType = new FloatType(dummyPos);
StdEnvironment.booleanType= new BooleanType(dummyPos);
StdEnvironment.stringType= new stringType(dummyPos);
StdEnvironment.voidType = new VoidType(dummyPos);
StdEnvironment.errorType = new ErrorType(dummyPos);
```

Note that `errorType.lol` can be assigned to an ill-typed expression.

#### Type Coercions

So there are really only two types of operations at a hardware level that use "+" that is integer addition (both operands are integers) and floating point addition, when both operands are reals.

But of course we don't want to create a language where `1+5.5` is illegal.

This is where `Type coercion` comes in, it is the name given to the process by which the compiler implicity converts int to float whenever necessary to have an expression evalaute. Because we do this the "+" operator is said to be overloaded for two operations, integer AND floating point addition.

Our assignment 4 should be able to handle this

#### Error Detection, Reporting and Recovery

Detection: we can detect an error via type rules
Reporting: we can print out menainful errors to help the coder
Recovery : we can continue checking types in the prescence of errors

the recovery bit is where things get interesting because we want to avoud a vascade of spurious errors that all stem from the same single bug.

So what we do is give a Illtyped expression a type of StdEnvironment.errorType
and then we do not report an error for an expression if any of its subexpressions is StdEnvironment.errorType. Thus for every expression we just list the first issue that arises and if more appear afterwards, later compilations will catch them.

## Ass 4
---

Job: Implement a one-pass semantic analyser using the visitor design pattern

Identification is implemented for you

Type checking is implemented by you
    - checking
    - adding int to float conversions where needed

Decorated ASTs:
    The synthesised attribute type in Expr nodes
    The synthesised attribute type in SimpleVar nodes

The symbol table discarded once the AST is decorated
