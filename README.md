# Flask YOLOv8 App (Dockerized)

This repository contains a simple Flask web application that uses **YOLOv8** for object detection.  
The application has been containerized with Docker for easy deployment.

---

## 📂 Project Structure

```

.
├── app.py              # Flask application entrypoint
├── yolov8m.pt          # YOLOv8 pretrained weights
├── requirements.txt    # Python dependencies
├── templates/          # Flask HTML templates
├── static/             # Static files (CSS, JS, images)
└── Dockerfile          # Docker build file

````

---

## 🐳 Build & Run with Docker

### 1. Build the Docker image
```docker build -t flask-yolo-app .```

### 2. Run the container

```docker run -d -p 5000:5000 flask-yolo-app```

* `-d` → Run in detached (background) mode
* `-p 5000:5000` → Map **host port 5000** → **container port 5000**

Now the app will be accessible at:
👉 [http://localhost:5000](http://localhost:5000)

---

## 🔍 Check Docker Images

```bash
docker images
```

You should see something like:

```
REPOSITORY       TAG       IMAGE ID       CREATED          SIZE
flask-yolo-app   latest    162ec232968d   X minutes ago    5.85GB
```

---

## 🛑 Stop & Remove Containers

### List running containers

```bash
docker ps
```

### Stop a container

```bash
docker stop <container_id>
```

### Remove a container

```bash
docker rm <container_id>
```

---

## ⚡ Notes

* YOLOv8 model weights (`yolov8m.pt`) are included inside the container.
* Flask app runs with:

  ```python
  app.run(host="0.0.0.0", port=5000)
  ```
* You can modify `requirements.txt` to add or remove dependencies, then rebuild the image.
