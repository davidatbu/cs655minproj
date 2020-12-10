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
def classify(session, indx):
    url = " http://192.171.20.116:8000"
    files = {'file': open('./dog.jpg', 'rb')}
    start_time_var = default_timer()
    with session.post(url,files=files) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(data))

        elapsed = default_timer() - start_time_var
        total_delays.append(elapsed)
        #link utilization
        time_completed_at = "{:5.2f}s".format(elapsed)
        #print("{0:<30} {1:>20}".format(indx, time_completed_at))
        return data

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

def main(n_requests):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(n_requests))
    loop.run_until_complete(future)
    print(np.mean(total_delays))
    
main(n_of_parallel_request)