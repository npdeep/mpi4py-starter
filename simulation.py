"""
Code for actual simulation
"""
import numpy as np


"""
SAMPLE SIMULATION:
I am going to implement a very dumb simulation. 

Given simulation paramters (mean, std, N)
- take N samples from a normal distribution. X ~ N(mean, std)
- compute the squares of the samples Y = X^2
- return the mean and variance of (Y). 
"""


"""
It is helpful to create a class that contains all the parameters needed for a simulation.
"""
class SimulationParams:
    def __init__(self, mean, std, n):
        """
        Get parameters for a
        :param mean: Mean of a normal distribution
        :param std: Standard Deviation of the normal distribution
        :param n: Number of samples to take
        """
        self.mean = mean
        self.std = std
        self.n = n

    def __repr__(self):
        return f"Mean: {self.mean}  Variance: {self.std}   N: {self.n}"

    def __str__(self):
        return self.__repr__


def simulate(params: SimulationParams):
    """
    Function to run the actual simulation.
    :param params: Simulation Parameters
    :return: estimated (mean, variance) of Y = X^2 for X ~ N(0, 1)
    """

    samples = np.random.normal(params.mean, params.std, params.n)
    samples_sq = np.square(samples)

    return np.mean(samples_sq), np.std(samples_sq)
