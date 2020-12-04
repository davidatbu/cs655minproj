import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
import sched, time
s = sched.scheduler(time.time, time.sleep)

def classify(session, indx):
    url = " http://127.0.0.1:8000"
    files = {'file': open('./dog.jpg', 'rb')}
    start_time_var = default_timer()
    with session.post(url,files=files) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(data))

        elapsed = default_timer() - start_time_var
        time_completed_at = "{:5.2f}s".format(elapsed)
        print("{0:<30} {1:>20}".format(indx, time_completed_at))
        return data

async def get_data_asynchronous():
    n_requests  = 10
    print("{0:<30} {1:>20}".format("File", "Completed at"))
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

def main(sc):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)
    s.enter(1, 1, main, (sc,))

s.enter(0, 1, main, (s,))
s.run()
