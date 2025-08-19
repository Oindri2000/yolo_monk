
from flask import Flask, request, jsonify, render_template, send_from_directory
from ultralytics import YOLO
import cv2
import numpy as np
import base64
import json
import os
from datetime import datetime

app = Flask(__name__)

# Paths
OUTPUT_DIR = "static/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load YOLOv8 model (small and CPU-friendly)
model = YOLO("yolov8m.pt")
HUMAN_CLASS_ID = 0  # YOLO's default for 'person'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    img_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    # Run YOLO detection
    results = model(img, conf=0.5)
    detections = []

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            if cls_id == HUMAN_CLASS_ID:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({
                    "class": "person",
                    "confidence": round(conf, 2),
                    "bbox": [x1, y1, x2, y2]
                })
                # Draw bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, f"Person {conf:.2f}", (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Create unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_filename = f"result_{timestamp}.jpg"
    json_filename = f"result_{timestamp}.json"

    # Save image
    img_path = os.path.join(OUTPUT_DIR, img_filename)
    cv2.imwrite(img_path, img)

    # Save JSON
    json_path = os.path.join(OUTPUT_DIR, json_filename)
    with open(json_path, "w") as f:
        json.dump({"detections": detections}, f, indent=4)

    # Encode image to display in browser
    _, buffer = cv2.imencode('.jpg', img)
    encoded_image = base64.b64encode(buffer).decode('utf-8')

    return jsonify({
        "detections": detections,
        "image": encoded_image,
        "image_file": img_filename,
        "json_file": json_filename
    })

@app.route('/download/<filetype>/<filename>')
def download_file(filetype, filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

