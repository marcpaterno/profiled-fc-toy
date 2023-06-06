"""
Generate and fit a toy pseudoexperiment.
"""

import math
import random
import numpy
from numpy.random import default_rng
import scipy

random.seed(137)  # for reproducibility
np_rng = default_rng(12345)  # for reproducibility

# Module data: these are values that were pre-determined for this use.
# See the README.md file for some explanation

# The values used for generating pseudoexperiments

A = 10.26
dA = 0.3
B = 5.16
dB = 0.1
C = 3.31
dC = 0.6
D = 0.76
dD = 0.04

# The number of bins in our energy spectra
N_b = 20

# The experiment's observed energy spectrum
OBS = [7, 4, 4, 3, 4, 6, 5, 3, 6, 5, 4, 1, 3, 0, 1, 1, 2, 0, 1, 0]


class LogLike:
    """LogLike is an encapsulation of the (negative) log likelihood function.
    It contains as state the "data" for which this is the likelihood."""

    def __init__(self, data):
        self.data = data

    def __call__(self, x):
        """Return the negative log likelihood for the encapsulated data,
        for the given set of parameter values in the numpy array `x`.
        N.B.: This is grossly inefficient, and is only being done
        here to keep most of the code in 'normal' Python, rather than using
        numpy.
        """
        return self.negative_log_likelihood(*list(x))

    def negative_log_likelihood(self, a, b, c, d, mass, delta):
        """Return the value of lambda for given set of model parameters,
        and for the fixed data in OBS.

        Note that having the data fixed in OBS is a clear hack. One more robust
        solution would be to introduce as class, to have those data in an
        instance variable, and to make this function into a method of the
        class.
        """
        bin_poisson_means = [
            poisson_mean_model(a, b, c, d, mass, delta, k)
            for k in range(1, N_b + 1)
        ]

        bin_log_likelihoods = [
            mu - d * math.log(mu) + math.log(numpy.math.factorial(d))
            for mu, d in zip(bin_poisson_means, self.data)
        ]
        return sum(bin_log_likelihoods)


def poisson_mean_model(a, b, c, d, mass, delta, k):
    """Generate the Poisson mean for bin k, for the given set of parameter
    values.
    """
    background = a * math.exp(-k / b) + d
    signal = (c / delta) * math.exp(-0.5 * ((k - mass) / delta) ** 2)
    return background + signal


def generate_pseudoexperiment(m, Delta):
    """Generate a random array of bin counts (a pseudoexperiment) for one
    pseudoexperiment, at the location (m, Delta) in our parameter space.
    """
    current_A = random.normalvariate(A, dA)
    current_B = random.normalvariate(B, dB)
    current_C = random.normalvariate(C, dC)
    current_D = random.normalvariate(D, dD)
    current_means = [
        poisson_mean_model(
            current_A, current_B, current_C, current_D, m, Delta, k
        )
        for k in range(1, N_b + 1)
    ]
    # We are not using numpy's ability to generate an array of variates
    # in a single call because we are trying to have a "pure python"
    # solution. However, since Python does not have a built-in Poisson
    # random number generate, we use one from numpy.
    # N.B.: this is not how we would use this generator if we were
    # trying to write efficient code.
    generated_counts = [np_rng.poisson(bin_mean) for bin_mean in current_means]
    return generated_counts


def fit_pseudoexperiment(data):
    """Given pseudoexperiment data (a list of counts in energy bins), find the
    minimum of the negative log likelihood and return it.
    """
    loglike = LogLike(data)
    initial_guess = numpy.array([10.0, 5.0, 3.0, 1.0, 8.0, 2.0])
    fit_result = scipy.optimize.minimize(loglike, initial_guess)
    return fit_result


def generate_one_fit(m, Delta):
    """Generate a single fit to the log likelihood, by generating and fitting
    one pseudoexperiment.
    """
    pe = generate_pseudoexperiment(m, Delta)
    fit = fit_pseudoexperiment(pe)
    return fit.fun


if __name__ == "__main__":
    # Pick a spot in our parameter space
    m, Delta = 8.0, 2.0

    fit = generate_one_fit(m, Delta)
    print(f"fit result: {fit}")
