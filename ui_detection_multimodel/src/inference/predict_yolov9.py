from ultralytics import YOLO

def predict():
    # Load your trained model
    model = YOLO("models/yolov9/final_yolov9_ui.pt")

    # Run inference
    results = model.predict(
        source="test_images/",   # folder with test images
        conf=0.25,
        save=True
    )

    print("Prediction complete")

if __name__ == "__main__":
    predict()