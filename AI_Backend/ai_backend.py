# ai_backend.py
import torch
import os
import json
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from PIL import Image

# =============== SETUP ===============
app = FastAPI(title="AI Backend - Object Detection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("outputs/images", exist_ok=True)
os.makedirs("outputs/json", exist_ok=True)

model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
model.to("cpu")


@app.get("/")
def root():
    return {"status": "AI backend is running", "endpoints": ["/predict/"]}


def run_inference(image_path: str):
    """Run YOLO inference on an image and save outputs."""
    results = model(image_path)

    detections = []
    for *xyxy, conf, cls in results.xyxy[0]:
        cls_id = int(cls)
        cls_name = results.names[cls_id]
        detections.append({
            "class_id": cls_id,
            "class": cls_name,
            "confidence": float(conf),
            "bbox": {
                "xmin": float(xyxy[0]),
                "ymin": float(xyxy[1]),
                "xmax": float(xyxy[2]),
                "ymax": float(xyxy[3])
            }
        })

    uid = str(uuid.uuid4())
    out_img = f"outputs/images/{uid}.jpg"
    out_json = f"outputs/json/{uid}.json"

    # Save annotated image directly
    results.render()
    for im in results.ims:
        im_pil = Image.fromarray(im)
        im_pil.save(out_img)

    with open(out_json, "w") as f:
        json.dump(detections, f, indent=4)

    return {"detections": detections, "image_path": out_img, "json_path": out_json}


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    temp_path = Path(f"temp_{file.filename}")
    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_inference(str(temp_path))

    temp_path.unlink(missing_ok=True)
    return JSONResponse(content=result)
