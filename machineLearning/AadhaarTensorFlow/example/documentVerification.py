import os
import json
import numpy as np
from threading import Lock
import tensorflow as tf
from PIL import Image
import cv2
import pytesseract
import re

class TFModel:
    def __init__(self, dir_path) -> None:
        self.model_dir = os.path.dirname(dir_path)
        with open(os.path.join(self.model_dir, "signature.json"), "r") as f:
            self.signature = json.load(f)
        self.model_file = os.path.join(self.model_dir, self.signature.get("filename"))
        if not os.path.isfile(self.model_file):
            raise FileNotFoundError(f"Model file does not exist")
        self.inputs = self.signature.get("inputs")
        self.outputs = self.signature.get("outputs")
        self.lock = Lock()
        self.model = tf.saved_model.load(tags=self.signature.get("tags"), export_dir=self.model_dir)
        self.predict_fn = self.model.signatures["serving_default"]

    def predict(self, image: Image.Image) -> dict:
        image = self.process_image(image, self.inputs.get("Image").get("shape"))
        with self.lock:
            feed_dict = {list(self.inputs.keys())[0]: tf.convert_to_tensor(image)}
            outputs = self.predict_fn(**feed_dict)
            return self.process_output(outputs)

    def process_image(self, image, input_shape) -> np.ndarray:
        if image.mode != "RGB":
            image = image.convert("RGB")
        width, height = image.size
        if width != height:
            square_size = min(width, height)
            left = (width - square_size) / 2
            top = (height - square_size) / 2
            right = (width + square_size) / 2
            bottom = (height + square_size) / 2
            image = image.crop((left, top, right, bottom))
        input_width, input_height = input_shape[1:3]
        if image.width != input_width or image.height != input_height:
            image = image.resize((input_width, input_height))
        image = np.asarray(image) / 255.0
        return np.expand_dims(image, axis=0).astype(np.float32)

    def process_output(self, outputs) -> dict:
        out_keys = ["label", "confidence"]
        results = {}
        for key, tf_val in outputs.items():
            val = tf_val.numpy().tolist()[0]
            if isinstance(val, bytes):
                val = val.decode()
            results[key] = val
        confs = results["Confidences"]
        labels = self.signature.get("classes").get("Label")
        output = [dict(zip(out_keys, group)) for group in zip(labels, confs)]
        sorted_output = {"predictions": sorted(output, key=lambda k: k["confidence"], reverse=True)}
        return sorted_output
config = {
    'PAN': re.compile(r'[A-Z]{5}[0-9]{4}[A-Z]{1}'),
    'AADHAR': re.compile(r'\d{4}\s?\d{4}\s?\d{4}'),
    'Aadhaar': re.compile(r'\d{4}\s?\d{4}\s?\d{4}')  
}
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (1000, int(image.shape[0] * (1000 / image.shape[1]))))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    preprocessed_image_path = 'processed_image.jpg'
    cv2.imwrite(preprocessed_image_path, thresh)

    return preprocessed_image_path
def extract_details(ocr_text, card_type):
    regex = config.get(card_type)
    if regex:
        matches = regex.search(ocr_text)
        return {
            'Number': matches.group(0) if matches else f'{card_type} Number not found'
        }
    return {'Number': f'Unsupported card type: {card_type}'}


def recognize_and_extract_card_details(image_path):
    try:
        
        dir_path = os.getcwd()
        tf_model = TFModel(dir_path=dir_path)
        
        
        image = Image.open(image_path)
        tf_output = tf_model.predict(image)
        
        
        highest_confidence_pred = tf_output['predictions'][0]
        predicted_type = highest_confidence_pred['label']
        confidence = highest_confidence_pred['confidence']

        processed_image_path = preprocess_image(image_path)

        ocr_text = pytesseract.image_to_string(Image.open(processed_image_path), lang='eng')

        os.remove(processed_image_path)

        details = extract_details(ocr_text, predicted_type)

        return {
            'Card Type': predicted_type,
            'Confidence': confidence,
            'Details': details
        }

    except Exception as e:
        return {'Error': str(e)}

image_path = './aadhar1.jpg'  

result = recognize_and_extract_card_details(image_path)
print(result)

if 'Error' in result:
    print("An error occurred. Here's some additional information:")
    print(f"Image path: {image_path}")
    print(f"Current working directory: {os.getcwd()}")
    print("Files in current directory:")
    print(os.listdir())
    print("Contents of signature.json:")
    try:
        with open("signature.json", "r") as f:
            print(json.load(f))
    except Exception as e:
        print(f"Could not read signature.json: {str(e)}")