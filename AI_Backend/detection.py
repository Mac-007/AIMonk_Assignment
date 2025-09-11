import torch
import cv2
import os
import json
import uuid

# Create output folders
os.makedirs("outputs/images", exist_ok=True)
os.makedirs("outputs/json", exist_ok=True)

# 1. Load YOLOv5 model (small, CPU)
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
model.to("cpu")   # force CPU

# 2. Input image (your URL or local path)
im = "https://images.pexels.com/photos/177809/pexels-photo-177809.jpeg"

# 3. Run inference
results = model(im)

# 4. Parse detections
detections = []
for *xyxy, conf, cls in results.xyxy[0]:  # xyxy = [x1, y1, x2, y2]
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

# 5. Save annotated image
uid = str(uuid.uuid4())
out_img = f"outputs/images/{uid}.jpg"
out_json = f"outputs/json/{uid}.json"

# Save image with bounding boxes drawn
results.save(save_dir="outputs/images")  # YOLOv5 auto-saves annotated image

# YOLO saves with original filename, so rename with uid
saved_file = os.path.join("outputs/images", os.path.basename(im).split("?")[0])
if os.path.exists(saved_file):
    os.rename(saved_file, out_img)

# 6. Save JSON
with open(out_json, "w") as f:
    json.dump(detections, f, indent=4)

print(f"[INFO] Annotated image saved at: {out_img}")
print(f"[INFO] JSON saved at: {out_json}")
