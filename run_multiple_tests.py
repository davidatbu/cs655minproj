import multiprocessing as mp
from time import sleep
from random import randint
import numpy as np
import subprocess
import sys 
from argparse import ArgumentParser
"""
argparser
"""
def parse_args():
    parser = ArgumentParser()

    parser.add_argument("--num_reqs", "-N", type=int, default = 10, help="Number of parallel requests in one run.")
    parser.add_argument("--time_between_runs", "-T", type=int, default=1, help="Seconds to wait between runs."
            " Note that the waiting starts right after the requests are fired (ie, the "
            " time the requests in the previous run take to be fulfilled does not affect "
            " the time between runs.")
    parser.add_argument("--runs", "-R", type=int, default=10, help="Total number of runs.")
    parser.add_argument("--verbose", "-V", action="store_true")
            
    args = parser.parse_args()

    return args.num_reqs, args.time_between_runs, args.runs, args.verbose
"""
This function calls test_script.py with the number of parallel request that
was passed to the function. We will later use this function as a trigger
to send parallel requests every N seconds 
"""

def function(N,i,returns_dict):
    bashCommand = "python3 test_script.py {}".format(N)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    returns_dict[i] = output

"""
Here we create a global list to store processes created and check if they are
finished or not and remove them from the list if they are.
This function essentially works in two parts
Part I 
It spawns a new multiprocessing process and calls function every n seconds
and it keeps checking if any processes are finished. If so it removes them
from the queue and keeps checking. If it had just spawned a new process it will
go into the wait loop where it will wait for T seconds to run another process
PART II
Finally when the total number of runs reach R it exits the while and just looks
at for processes that are finished. When they are all finished it exits and 
prints n and the average delay. 
"""

process_data_list = []
def main(N, sleep_timer, num_of_tries, verbose):

    run_next=True
    manager = mp.Manager()
    returns_dict = manager.dict()
    times_index = 0
    while times_index < num_of_tries:

        # cleanup stopped processes -------------------------------
        cleanup_done = False
        while not cleanup_done:
            cleanup_done = True
            # search stopped processes
            for i, process_data in enumerate(process_data_list):
                if not process_data[1].is_alive():
                    if verbose:
                        print(f'process {process_data[0]} finished')
                    # remove from processes
                    p = process_data_list.pop(i)
                    del p
                    # start new search
                    cleanup_done = False
                    break

        # try start new process ---------------------------------
        if run_next:
            process = mp.Process(target=function,args = [N,times_index,returns_dict])
            process.start()
            process_data_list.append([times_index, process])
            if verbose:
                print(f'process {times_index} started')
            times_index += 1
            run_next = False
        else:
            sleep(sleep_timer)
            run_next = True

    # wait for all processes to finish --------------------------------
    while process_data_list:
        for i, process_data in enumerate(process_data_list):
            if not process_data[1].is_alive():
                if verbose:
                    print(f'process {process_data[0]} finished')
                # remove from processes
                p = process_data_list.pop(i)
                del p
                # start new search
                break

    #print('ALL DONE !!!!!!')
    return returns_dict

# =======================================================================================
n, sleep_timer, num_of_tries, verbose = parse_args()
returns_dict = main(n, sleep_timer, num_of_tries, verbose)
total_delays = []
for i,value in returns_dict.items():
    try:
        total_delays.append(float(value.decode("utf-8").split("\n")[0]))
    except:
        print("error in process {}".format(i))
print(n,np.mean(total_delays))
