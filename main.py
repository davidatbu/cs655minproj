from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from PIL import Image
import torch
import torchvision
import json
import io

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

model = torchvision.models.resnet18(pretrained=True)
model.eval()

# Image transforms
normalize = torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                             std=[0.229, 0.224, 0.225])
transform = torchvision.transforms.Compose([
    torchvision.transforms.Resize(256),
    torchvision.transforms.CenterCrop(224),
    torchvision.transforms.ToTensor(),
    normalize,
])

with open('label_map.json', 'r') as f:
    label_map = json.load(f)

@app.get("/")
async def main_page():
    return RedirectResponse("/static/index.html")

@app.post("/")
async def predict(file: UploadFile=File(...)):
    contents = await file.read()
    img = transform(Image.open(io.BytesIO(contents)).convert('RGB')).unsqueeze(0)
    cl_idx = model(img).argmax(dim=1).squeeze()
    cl_label = label_map[str(cl_idx.item())][1]
    return cl_label
