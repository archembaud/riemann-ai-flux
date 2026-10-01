# 1D Survey Results

## Shock Tube Problem

Using a standard 1D shock tube problem, the breakdown is:


### Right to Left Shock Tube

Breakdown of types:

```bash
Type_count[0] = 0
Type_count[1] = 0
Type_count[2] = 74564
Type_count[3] = 0
Type_count[4] = 0
Type_count[5] = 7
```


### Left to Right Shock Tube

Breakdown of type:

```bash
Type_count[0] = 0
Type_count[1] = 0
Type_count[2] = 74564
Type_count[3] = 0
Type_count[4] = 7
Type_count[5] = 0
```

Vast majority of this problem is type 2 according to our code.

### Shu-Osher 1D Benchmark (standard)

The initial conditions are: 

L = 10

If x < 1, (den, U, pressure) = (3.857134,2.629369,10.33333)
Else: (1 +0.2sin(5x),0,1)

Breakdown of problem types:

```bash
Type_count[0] = 0
Type_count[1] = 0
Type_count[2] = 133191
Type_count[3] = 0
Type_count[4] = 1680
Type_count[5] = 0
```

So it looks like the vast majority is 2, and the current definition of types might not be so helpful.