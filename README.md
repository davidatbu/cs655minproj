# Installation

```bash
$ pip install -r requirements.txt
```

# Running

```bash
uvicorn main:app --reload
```

Then use a web browser to access:

```
http://IP:8000/
```

And follow the prompts to upload a file and submit to get a classification.


You can also use the command line. While the server is running, use `curl` like the following:

```bash
$ curl -X POST --form file=@/path/to/image.extension IP:8000
```
Above, `IP` refers to the public IP of the server, which can be replaced with `localhost`, if the client is being run on the same machine as the server. 


# Testing

There are two test scripts.

The first script will create N parallel workers. Each worker will submit a post request, sending an image and waiting for the response. It will start a timer and, in the end, return the time taken to fulfill the request. The script takes one parameter "N", which is the number of parallel requests. Run it like so:

```bash
$ python test_script.py N
```

For example:

```bash
$ python test_script.py 10
```

This will spawn 10 parallel requests.


In the second test script, requests don’t wait for each other and achieve true parallelism and scheduling. The code creates an empty processes list and assigns a new one each T second and clears finished processes. There is no explicit limit to the number of processes that can be created. We might test for higher levels of parallel requests with lower number of Ts. This makes sure that the client side would not bottleneck the testing and the server side could be pushed to its limits. Run the test script like so:

```bash
$ python run_multiple_tests.py -N N -T T -R R -V 
```

N is the number of (parallel) requests to be run in parallel.

T is the amount of time in seconds to wait after spawning the N requests. T has to be an integer.

For R, this process will be repeated R times.

-V is for verbosity.

All arguments are optional.

So as an example:

```bash
$ python run_multiple_tests.py -N 10 -T 1 -R 5
```

Here, the script will spawn 10 requests in parallel, wait for 1 second, spawn 10 more requests, wait for 1 second, spawn 10 more requests ... 5 times.
