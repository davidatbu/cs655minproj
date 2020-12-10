import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
import sched, time
import numpy as np
import sys 
args = sys.argv
n_of_parallel_request = int(args[1])

total_delays = []
repetitions = 0
"""
This function takes a session from the requests library and an index and will
return the data that returned by the server. In the mean time it will measure
the time required to process one request and append this value to a shared 
list parameter 
"""
def classify(session, indx):
    url = " http://localhost:8000"             # Here we declare the destination IP and port
    files = {'file': open('./dog.jpg', 'rb')}
    start_time_var = default_timer()                # We start the timer 
    with session.post(url,files=files) as response: # Here use the given session and send a post request
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(data))      # Here if the server doesn't return code 200 we print an error

        elapsed = default_timer() - start_time_var  #once we get the response we take the elapsed time
        total_delays.append(elapsed)

        #time_completed_at = "{:5.2f}s".format(elapsed)
        #print("{0:<30} {1:>20}".format(indx, time_completed_at))
        return data
"""
This function creates creates n parallel workers and runs the classify function
in parallel. The word classify here is used from the users point of view where
They will want to classify images. 
Here we use the threadpoolexecutor to create independent runs.  
"""
async def get_data_asynchronous(n_requests):
#    n_requests  = 10
    #print("{0:<30} {1:>20}".format("File", "Completed at"))
    with ThreadPoolExecutor(max_workers=n_requests) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    classify,
                    *(session, indx) 
                )
                for indx in range(n_requests)
            ]
            for response in await asyncio.gather(*tasks):
                pass
"""
The main function creates an asyncio event loop and runs the function aboe
untill it is complete and prints the mean delay for this run.
the printing part is important because we will call this function
as a bash script from run_multiple_test and we can get as result what this 
function prints out.
"""
def main(n_requests):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(n_requests))
    loop.run_until_complete(future)
    print(np.mean(total_delays))
    
main(n_of_parallel_request)
