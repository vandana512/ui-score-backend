from ultralytics import YOLO

def train():
    model = YOLO("models/yolov9/yolov9m.pt")

    model.train(
        data="data/data.yaml",
        epochs=100,
        imgsz=640,
        batch=16,
        name="yolov9_ui"
    )

if __name__ == "__main__":
    train()