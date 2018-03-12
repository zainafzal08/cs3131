# Java Byte Code Generation

## Intro
---

The final step, the final countdown. This is what the Jasmin Assembler produces, java bytecode perfect for running on any JVM. 

## Object Code Generation for Register-Based Machines
---

There are three issues with this.
1. having to handle register allocation
2. instruction selection
3. code scheduling

For stack based machines this is easily especially if the quality of the generated code is not a concern. I.e we arn't trying to optimise heavily. 

If we did then we would do Advanced Comiler COnstruction with code optimisation, Object code generation for register-based machines and Research topics. 

## Example compilation
---

So jasmin is for java, not VC so we have to tweek it a bit. Given the follwing code in a file called gcd.vc

```c
int i = 2;
int j = 4;
int gcd(int a, int b) {
  if (b == 0)
  return a;
else
  return gcd(b, a - (a/b) *b);
}
int main() {
  putIntLn(gcd(i, j));
  return 0;  // optional in VC or C/C++
}
```

We have some stuff that we assume / add in here so we can jasmin it. 

```java
public class gcd {
    static int i = 2;
    static int j = 4;
    public gcd() { } // the default constructor

    int gcd(int a, int b) {
        if (b == 0)
            return a;
        else
            return gcd(b, a - (a/b) *b);
    }

    void main(String argv[]) 
        gcd vc$;
        vc$ = new gcd();
        System.putIntLn(vc$.gcd(i, j));
        return;
    }
}
```

I.e wrapping the file into a class, making global variables become class wide variables, and having any functions run from a instance of the class. 

Also it changes main from a int to a void. Note all built in VC functions are static. 

Anyway once we have this form we just run through and get the jasmin out. 
We can do this via using the Code Generator as a Vicitor Object

## Code Generator
---

Our code generator traverses the AST to emit code in pre, in or post order. 

Emitter.java:       The visitor class for generating code
JVM.java:           The class defining the simple JVM used
Instruction.java:   The class defining Jasmin instructions
Frame.java:         The class for info about labels, local
                    variable indices, etc. for a function

#### Code Template

lets set this symbol `[[x]]` to represent the code generator for `x`

a code template is just a set of generic jasmin code fragments for a given peice of code x and should translate the construct indepdnently of the context in which it is used. Of course by ignroing context we get less efficient and optimised code BUT this can be optimised later. 

#### Expressions

A simple code template for `[[INTLITERAL]]` could be a function called `emitICONT` as such

```java
private void emitICONST(int value) {
  if (value == -1)
  emit(JVM.ICONST_M1);
else if (value >= 0 && value <= 5)
  emit(JVM.ICONST + "_" + value);
else if (value >= -128 && value <= 127)
  emit(JVM.BIPUSH, value);
else if (value >= -32768 && value <= 32767)
  emit(JVM.SIPUSH, value);
else
    emit(JVM.LDC, value);
}
```

which can then be called by the vistor method `visitIntLiteral` which can then `emit` the code!!

Floating point can be done similarly. 

Booleans are interesting because it basically becomes this, given that True and False are just 1 and 0. 

```java
private void emitFCONST(boolean value) {
    if (value)
        emit(JVM.ICONST_1);
    else
        emit(JVM.ICONST_0);
}
```

note that with the vistior methods the frame is passed in via object o

 ```java
public Object visitBooleanLiteral(BooleanLiteral ast, Object o) {
  Frame frame = (Frame) o;
  emitBCONST(ast.spelling.equals("true"));
  ...
  return null;
}
 ```

Now aritmatic expressions get fun because `[[E1 i+ E2]]` is the same as `[[E1]] [[E2]] emit("iadd")`

meaning at the start of the visit function you just visit both and then check which addition it is and run the relevent command. 

With realational expressions we just compare and get either 0 or 1 at the top of the stack to be treated like a boolean in any statement following. 

```
    [[E1 ]]
    [[E2 ]]
    if icmpgt L1
    iconst 0
    goto L2
L1:
    iconst 1
L2:
```

Note that there is no `if_cmpgt` and must be simulared by `fcmpg` and `ifgt`

Note that when we do `a=b=1` we need to know the context in which `b=1` is used, we can do so via the parent links in every AST node. 

## Frames
---

So a new frame object is created everytime visitFuncDecl is called. 

We can use this to keep track of stuff like labels. 

<img src="D_1.png" style="width: 400px">

Remember that we must obey the rule of short-circuit evaluation

```java
boolean f() {
  putBool(false);
  return false;
}
void main() {
    // f() shouldn't run
    // false && anything is false. 
  false && f();
}
```

## Statements
---

#### If 
note that with if statements treat eveyr single one as if it is a if else, if there is no else just have [[s2]] be empty and the templete will still work fine

```
    [[E1]]
    ifeq L1
    [[S1]]
    goto L2
L1:
    [[S2]]
L2:
```

#### While

with while we Push the continue label L1 to conStack and Push the break label L2 to brkStack and then pop these off once the loop is over. 
The loop works as expected with a check and then the statement then a goto back to the top to be checked again. 

When you hit a break or continue you goto the label marking the end or the start of loop. note the pop's are after the loop ends so if you jump the end of the loop it should automatically pop off the breaks and continues before continuing. 

#### Expr stmts
Note that with expression statements we do 

```
[[E]]
pop        ; if it has a value left on the stack
```

stuff like a function call with it's result neing not assigned to anything should have the return value it put onto the stack popped off after it is done. 

#### Compound stmts

With compound statements we have to push and pop the labels marking the beginning of the scope and the end of the scope. 

#### Global Vars

These just generate .field declerations. (All initialisers for global variables are assumed to be constant expressions as in C, although this was not checked in Assignment 4)

#### Local Vars

Instance field index available in VC.ASTs.Decl.java

Call frame.getNewIndex() to allocate indices
consecutively for formal parameters and local variables:

For a function (treated as an instance method), 0 is
allocated to this

For main (a static method), 0 is allocated argv and 1 to the implicitly declared variable vc$. 

#### Directives

We generate the `.limit locals` after the function has been processes as then we know everything. it ends up being `.limit locals X` where X is the current value of frame.getNewIndex()

We also use `.var` when a var or formal para decl is processed. We get most of the information for this line from the Decl node. the scopeStart and scopeEnd labels are from the frame stacks. 

`.line` should be obvious but is also optional, do it at the end if you have the time it isn't really needed. you need a good source position to be able to handle this. 

the `.limit stack` is harder, we basically need to simulate the execution of the bytecode generated and count the max depth the stack get's to 

#### Note

• Java byte code requires that
• all variables be initialised
• all method be terminated by a return
• Both are not enforced in the VC language
• All test cases used for marking Assignment 5 will satisfy
the 1st restriction,
• You can satisfy the 2nd restriction by either having approprite returns in your test programs or optionally forcing your VC compiler to always generate an appropriate return for each function















