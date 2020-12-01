from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/")
async def root(file: UploadFile=File(...)):
    contents = await file.read()
    print(f"Received a file of with name: {file.filename} and size: {len(contents)}")
    return "dog"
