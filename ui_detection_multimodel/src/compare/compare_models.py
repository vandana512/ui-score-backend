from utils.helpers import load_results

def compare():
    print("\n=== MODEL COMPARISON ===\n")

    try:
        y8 = load_results("results/yolov8_results.json")
        print("YOLOv8:", y8["overall"])
    except:
        print("YOLOv8 results not found")

    try:
        y9 = load_results("results/yolov9_results.json")
        print("\nYOLOv9:", y9["overall"])
    except:
        print("YOLOv9 results not found")

    try:
        frcnn = load_results("results/faster_rcnn_results.json")
        print("\nFaster R-CNN:", frcnn["overall"])
    except:
        print("Faster R-CNN results not found")

    print("\nInsights:")
    print("- YOLOv8: fast baseline")
    print("- YOLOv9: better accuracy")
    print("- Faster R-CNN: slower, struggles on UI data")

if __name__ == "__main__":
    compare()