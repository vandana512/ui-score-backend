import yaml
import os
import json

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_class_names():
    data = load_yaml("data/data.yaml")
    return data["names"]

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_results(results, path):
    with open(path, "w") as f:
        json.dump(results, f, indent=4)

def load_results(path):
    with open(path, "r") as f:
        return json.load(f)

def print_dataset_info():
    data = load_yaml("data/data.yaml")
    print("\nDataset Info:")
    print("Classes:", data["names"])
    print("Train:", data["train"])
    print("Val:", data["val"])

