# Actuarial math life funtions


## Pure premium for  the annual life insurance's variations

The class ``life_insurance`` contains five variations of annual life insurance implemented. Consider the following variables:

* $i$: rate.
* $x$: age.
* $v$: discount factor: 

$$
v = \left(\dfrac{1}{1+i} \right)
$$

* $n$: years of contract.
* $m$: years of deffering.
* $\omega$: the maximum age a person can reach given according to a life table.

### The whole life insurance: 
$$
A_x = B \cdot \sum_{k=0}^{\omega - x} v^{k} {}_{k}p_{x} q_{x+k}
$$

### The term life insurance:
$$
A_{_{x}^{1}:\overline{n}|} = B \cdot \sum_{k=0}^{n} v^{k} {}_{k}p_{x} q_{x+k} \hspace{.5cm} \text{for } (n+x)<\omega
$$

### The deffered whole life insurance:

$$
{}_{m|}A_x = B \cdot v^{m} {}_{m}p_{x}  \cdot \sum_{k=0}^{\omega-x} v^{k} {}_{k}p_{x+m} q_{x+m+k} \hspace{.5cm} \text{for } (x+m)<\omega
$$

### The deffered term life insurance:

$$
{}_{m|}A_{_{x}^{1}:\overline{n}|} = B \cdot v^{m} {}_{m}p_{x}  \cdot \sum_{k=0}^{n} v^{k} {}_{k}p_{x+m} q_{x+m+k} \hspace{.5cm} \text{for } (x+m+n)<\omega
$$

### Pure Endowment

$$
{}_{n}E_{x} = A_{_{x}:{}_{\overline{n}|}^{1}} = B \cdot v^{m} {}_{m}p_{x}
$$

### Endowment

$$
A_{x:\overline{n}|} = B \cdot A_{_{x}:{}_{\overline{n}|}^{1}} + A_{_{x}^{1}:\overline{n}|}
$$

## Pure premium for  the annual annuities variations

