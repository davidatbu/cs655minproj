# Installation

```bash
$ pip install -r requirements.txt
```

# Running

```bash
uvicorn main:app --reload
```

# Testing
While the server is running, one can run `curl` to test it like the following:

```bash
$ curl --form file=@/home/davidat/Pictures/my_img.jpeg localhost:8000
```

The server will show some lines like the following

```
Received a file of with name: my_img.jpeg and size: 1173220
INFO:     127.0.0.1:50744 - "POST / HTTP/1.1" 200 OK
```
