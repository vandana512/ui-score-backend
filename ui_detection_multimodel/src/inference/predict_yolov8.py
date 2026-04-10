from ultralytics import YOLO

def predict():
    model = YOLO("models/yolov8/yolov8m.pt")
    # if trained:
    # model = YOLO("models/yolov8/final_yolov8_ui.pt")

    results = model.predict(
        source="test_images/",
        conf=0.25,
        save=True
    )

    print("YOLOv8 prediction complete")

if __name__ == "__main__":
    predict()