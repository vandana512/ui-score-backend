import torch
import cv2
from utils.helpers import get_class_names

def load_model(path):
    model = torch.load(path)
    model.eval()
    return model

def predict_image(model, image_path, threshold=0.5):
    image = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    img_tensor = torch.tensor(img_rgb / 255.0, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)[0]

    boxes = outputs["boxes"]
    scores = outputs["scores"]
    labels = outputs["labels"]

    classes = get_class_names()

    for i in range(len(boxes)):
        if scores[i] > threshold:
            x1, y1, x2, y2 = boxes[i].int().tolist()
            label = classes[labels[i]]

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    return image

def predict():
    model = load_model("models/faster_rcnn/final_faster_rcnn_ui.pth")

    image_path = "test_images/sample.jpg"

    result = predict_image(model, image_path)

    cv2.imwrite("output_frcnn.jpg", result)

    print("Faster R-CNN prediction complete")

if __name__ == "__main__":
    predict()