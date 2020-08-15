from mpi4py import MPI
from simulation import SimulationParams, simulate
import numpy as np


comm = MPI.COMM_WORLD;


def main(comm):
    """
    All processes execute this function.
    """

    if comm.rank == 0:
        """
        This is the master controller section of the code. 
        Here, we do the all the book-keeping. 
        
        The controller sends jobs to other processes.
        """

        # for example, I want to run the simulation for 5 different values for mean and
        # five different values for the standar deviation
        mean_s = np.linspace(0, 10, 5)
        std_s = np.linspace(0, 10, 5)
        n = 1000   # number of samples to take in each simultion

        # create a list for simulation params
        params_list = []
        for mean in mean_s:
            for std in std_s:
                params = SimulationParams(mean, std, n)
                params_list.append(params)

        # prepare to send the parameters to processes as jobs.
        # comm.size = Number of processes.
        # create a list of jobs for each process.
        jobs_list = [[] for _ in range(comm.size)]
        for k, params in enumerate(params_list):
            # distribute the jobs to all the processes evenly.
            jobs_list[k % comm.size].append(params)
    else:
        """
        If current process is not the controller, don't create any more jobs.
        """
        jobs_list = None

    # This is where we really scatter our jobs to processes
    my_work = comm.scatter(jobs_list)
    my_result = child_worker_job(my_work)
    # each process returns a list of results because we sent each processor a list of jobs.
    result_chunks = comm.gather(my_result)

    if comm.rank == 0:
        """
        Process the result
        """
        data = []
        for result_chunk in result_chunks:
            for result in result_chunk:
                # the first element is the simulation parameters we had transmitted earlier
                params = result[0]
                input_mean = params.mean
                input_std = params.std

                output_mean, output_std = result[1]

                data.append((input_mean, input_std, output_mean, output_std))

        # process the data as you like or write it to a file
        with open("simulation_data.txt", "w") as output_file:
            for row in data:
                output_file.write(str(row) + "\n")


def child_worker_job(params_list):
    """
    Each worker (process) receives a list of jobs to do.
    :param params_list: List of simulation parameters or jobs.
    :return: A list of output for each job.
    """
    result_list = []
    for params in params_list:
        # run the simulation and return the result together with the parameters
        result_list.append((params, simulate(params)))
    return result_list


if __name__ == "__main__":
    main(MPI.COMM_WORLD)
