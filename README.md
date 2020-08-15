Message Passing Interface on Python
---

This is a boilerplate code to run simulations on a multi-processor cluster using the message-passing interface.

I use the [MPI for Python](https://mpi4py.readthedocs.io/en/stable/) package to run my simulations in parallel.

Installation should be as easy as
```python
 pip install mpi4py
```
But if it doesn't work, consult the documentation for help.

### Simulating experiments across many jobs

In this repo, I demonstrate how to run a simple experiment across many processors and collect their output. To show this, I have a very simple experiment in mind.

The goal of the experiment is to study the properties of the distribution obtained by squaring the Normal distribution

`Y = X^2` where  `X ~ N(mu, sigma)`

Each experiment or a job takes in as parameters `(mu, sigma, N)`. 
We would like to take `N` samples from the normal distribution `X ~ N(0, 1)`. After collecting `N observations, we compute the square of the observation. 
Finally, we return the mean and standard deviation of the squared samples as output. 

We would like to do this for many values of `mu` and many values of `sigma`. 

A typical simulation is usually much complex than what I have described but this simple sampling experiment is adequate for this demonstration. 

### Code organization

The "message-passing interface" part of the code is in `main.py`. We may have a thousand different experiments. But the number of processor available is usually lower than that.
So, we first need to prepare a list of jobs for each processor to run independently. `main.py` does precisely that. It assigns processors jobs and collects responses from them.

The actual experiment happens in `simulation.py`. The experiment itself is very simple. It samples from a Normal distribution, and returns the mean and variance of square observations. 

 ### Running the simulation
 ```python
mpirun -n 4 python main.py
```
`n=4` gives the number of processors.