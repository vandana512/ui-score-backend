from ultralytics import YOLO

def train():
    model = YOLO("models/yolov8/yolov8m.pt")

    model.train(
        data="data/data.yaml",
        epochs=80,
        imgsz=640,
        batch=16,
        name="yolov8_ui"
    )

    print("YOLOv8 training complete")

if __name__ == "__main__":
    train()