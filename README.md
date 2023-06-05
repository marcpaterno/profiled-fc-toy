# A toy demonstration of the Profiled Feldman-Cousins Technique

This repository contains code to demonstrate the algorithms used in the
“Profiled Feldman-Cousins” technique for parameter and confidence
interval estimation. It is a *toy* demonstration in that the physical
model used is not motivated by any physics, and is very simple. The
actual problems to which this technique is applied are much more
complicated. The entire well-motivated and more more complex physical
models, and many more parameters.

## The toy physical model

Our toy physical model contains to major propositions:

1.  The process we are observing (the appearance of events with energy
    $x$ in our detector) is a Poisson process. This means the observed
    energy spectrum (the count of events in each energy bin) is an
    observation of a $N_b$ independent Poisson random variables, where
    $N_b$ is the number of bins in our spectrum.

2.  The Poisson mean $\mu_k$ for each bin $k$ (will will use $k$ to
    index energy bins) is:
    $$\mu_k = A e^{(-k/B)} + \frac{C}{\Delta} e^{-\frac{1}{2} (\frac{k-m}{\Delta})^2} + D$$

    $A$, $B$, $C$, $D$, $m$ and $\Delta$ each denote scalar values. We
    are interested in the parameters $m$ and $\Delta$; these are the
    parameters we are estimating. The parameters $A$, $B$, $C$ and $D$
    are nuisance parameters; they play a role in the “physics”, but we
    do not care about their values.

3.  The likelihood that we are maximizing is:
    $${\cal L} = \prod\limits_{k=1}^{N_b} P(d_k | \mu_k)$$ where
    $P(d_k | \mu_k)$ is the likelihood for observing $d_k$ events in a
    Poisson process with mean $\mu_k$:
    $$P(d|\mu) = e^{-\mu} \mu^d / d!$$

In the real neutrino experiments, the formula for $\mu_k$ is much more
complicated, and the likelihood has additional multiplicative terms. But
the toy shared the essential feature that the likelihood for the
observed data depends upon the unknown values of the parameters, both
the interesting ones and the nuisance parameters.

Because individual likelihoods can be quite small, it is common to work
with the natural logarithm of the likelihood. The likelihood has a
maximum where the log of the likelihood has a maximum. Finally, we
usually work with the *negative* of the log of the likelihood. The
finding of the maximum likelihood corresponds to minimization of the
negative log likelihood:

$$ \lambda = - \log({\cal L}) = \sum\limits_{k=1}^{N_b} ( \mu_k - d_k \mu_k + \log(d_k!)  )$$

Sometimes, Stirling’s approximation for $d_k!$ is introduced here, since
it is already quite accurate for $n=1$. The code in this repository does
*not* make this approximation.

Recall that $\lambda$ above is a function of the parameters of the model
($A$, $B$, $C$, $D$, $m$, and $\Delta$); these are the variables being
fitted. It is not a function of the data $\vec{d}$, which are not varied
— the data are whatever the experiment observed.

## Creating simulated data

Since we have not run a real physical experiment to collect data that we
can fit out our model, we need to generate some. This process is similar
(but not identical) to the process we’ll use for generating
pseudoexperiments.

First we need to specify the *true* values for the model parameters.
Note that this implies the proposition that our model is a faithful
model of physical reality. In this work, we are not *testing* that
proposition. We are asserting the proposition, and then given that
assertion, we are estimating the values of the parameters of interest of
the model.

<div id="tbl-param-truth">

| name  | value |
|:------|------:|
| A     |  10.2 |
| B     |   5.3 |
| C     |   3.5 |
| D     |   0.7 |
| m     |   8.3 |
| Delta |   1.8 |

Table 1: The true values for all the parameters in our model.

</div>

This set of parameters yields the following expected “shape” for the
spectrum. Note that this is a plot of the Poisson mean for each bin, not
the number of observed events in the simulated experiment (that we have
not yet simulated).

<img src="README_files/figure-commonmark/fig-true-mean-1.png"
id="fig-true-mean"
alt="Figure 1: True Poisson mean as a function of energy bin index" />

Finally, we generate $N_b$ Poisson random variates: the energy spectrum
of our simulated data. Our (simulated) spectrum is: 7, 4, 4, 3, 4, 6, 5,
3, 6, 5, 4, 1, 3, 0, 1, 1, 2, 0, 1, 0.

<img src="README_files/figure-commonmark/fig-observed-spectrum-1.png"
id="fig-observed-spectrum"
alt="Figure 2: Observed spectrum (for our simulated experiment)." />

## Profiling over nuisance parameters

When we perform a physics experiment, we do not know the true values of
the model parameters we are estimating. We sometimes have information
about at least some of the parameters. Often this information takes the
form of estimated values and uncertainties for those parameters. In this
case, we will assume we have such information — from some other source,
not from our experiment — for all our nuisance parameters. We will
assume the following values and uncertainties when we are doing the
profiling over the nuisance parameters.

| name |  mean |   sd |
|:-----|------:|-----:|
| A    | 10.26 | 0.30 |
| B    |  5.16 | 0.10 |
| C    |  3.31 | 0.60 |
| D    |  0.76 | 0.04 |
