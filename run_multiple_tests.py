import multiprocessing as mp
from time import sleep
from random import randint
import numpy as np
import subprocess
import sys 
args = sys.argv
try:
    n = int(args[1])
except:
    print('Number of parallel runs not given. Setting to default:10')
    n = 10
try:
    sleep_timer = int(args[2])
except:
    print('Time betweeen triggers not given. Setting to default:1')
    sleep_timer = 1
try:
    num_of_tries = int(args[3])
except:
    print('Number test runs not given. Setting to default:10')
    num_of_tries = 10
try:
    verbose = int(args[4])
except:
    print('Number test runs not given. Setting to default:10')
    num_of_tries = False

def function(N,i,returns_dict):
    bashCommand = "python3 test_script.py {}".format(N)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    returns_dict[i] = output


process_data_list = []
def main(N):
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
returns_dict = main(n)
total_delays = []
for i,value in returns_dict.items():
    try:
        total_delays.append(float(value.decode("utf-8").split("\n")[0]))
    except:
        print("error in process {}".format(i))
print(n,np.mean(total_delays))
