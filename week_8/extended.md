# Code Optimisation

## Intro

The purpose of Optimisation is to take code that crummy programmers write and reduce the size of the executable while also trying to increase the speed of the code.


## Basic Dead Code Elimination

basic control flow structures give rise to trees which can be pruned

```
if(1) {
  // do this
} else {
    // do this
}
```

A common optimisation here is to remove the else from the code entirely.

Observe

```
int x = myFunction();
return EXIT_SUCCESS;
```

In some instances the function is removed from the code entirely because it's value is never used.

## loops and redundancy

Often times coders will write something such as

```c
j = 0;
while(j<MAX) {
  i = 0;
  j++;
}
```

Here the i variable is reassigned every single iteration of the loop where it really doesn't matter. This would be better written as

```c
j = 0;
i = 0;
while(j<MAX) {
  j++;
}
```

To reduce the amount of operations done. This is called code movement.

Furthermore you will also see

```c
int i = 0;
int j = 1;
int k = i + j;
...
```

This is often reduced to eliminate uneeded variables into something like

```
int k = 0+1;
```

this is called constant propergation
and closely related is constant folding which is

`int k = 0+1+2+3 -> int k = 6`


## Sub expression Elimination

similar to the above example if a expression appears multiple times, the compiler will try to reduce repeated calculations, if in a certain scope a expressions variables have not changed it will be propergated as a constants


```c
int b = 1;
int c = 1;
printf("1+1 is %d",b+c);
printf("1+1 is still %d",b+c);
printf("1+1 is guess what? %d",b+c);
b=3;
printf("1+3 is %d",b+c) // recalculate
```

## Strength Reduction

This is very algos like, doing a generic mult operation such as

`A*2`

is more expencive then

`A+A`

so compilers will try and convert code into the latter.

another example is

`A*8 -> A<<3`

## How

Constant Folding on an AST

` x := y + 1 + 2 + z; -> x := y + 3 + z;`

```
  :=
 /  \
x    +
    / \
   +   z
  / \
 +   2
/ \
y   1

```

Do a R rotation

```
  :=
 /  \
x    +
    / \
   +   z
  / \
 y   +
    / \
   2   1

```

Nip

```
  :=
 /  \
x    +
    / \
   +   z
  / \
 y   3

```
