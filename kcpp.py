import requests
import base64
import json
import time
from PIL import Image
from io import BytesIO

def _convert_image_to_b64_(image_path):
    QUALITY_FACTOR = 100
    img = Image.open(image_path)
    rgb_img = img.convert("RGB")
    # Resize the image (optional)
    new_width = 512
    new_height = 512
    resized_img = rgb_img.resize((new_width, new_height))
    # Save the image to a BytesIO object
    byte_io = BytesIO()
    resized_img.save(byte_io, format="JPEG", quality=QUALITY_FACTOR, optimize=True)
    # Get the byte data and returning them
    image_bytes = byte_io.getvalue()
    image_base64_string = base64.encodebytes(image_bytes)
    return image_base64_string


'''
An API for koboldcpp
'''


class KoboldCppTextGen:
    SERVER_URL = "http://127.0.0.1:8080/api/v1/generate"

    def __init__(self, server_url=SERVER_URL):
        self.server_url = server_url
        self.default_payload = {
            "max_context_length": 2048,
            "max_length": 300,
            "prompt": "",
            "quiet": True,
            "rep_pen": 1.1,
            "rep_pen_range": 320,
            "rep_pen_slope": 0.7,
            "temperature": 0.7,
            "tfs": 1,
            "top_a": 0,
            "top_k": 100,
            "top_p": 0.92,
            "typical": 1,
            "sampler_order": [6, 0, 1, 3, 4, 2, 5],
            "min_p": 0,
            "dynatemp_range": 0,
            "dynatemp_exponent": 1,
            "smoothing_factor": 0,
            "presence_penalty": 0,
            "images":[]
          }

    def generate_text(self, prompt_string):
        self.default_payload['prompt'] = prompt_string
        response = requests.post(self.server_url, json=self.default_payload)
        self.dict_response = json.loads(response.text)['results'][0]
        self.dict_response_text = self.dict_response['text']
        return self.dict_response_text
    
    def attach_image_simple(self, image_path):
        image_string_to_add = str(_convert_image_to_b64_(image_path), "utf-8").replace('\n','')
        self.default_payload["images"].append(image_string_to_add)

    def set_max_length(self, max_length=300):
        self.default_payload["max_length"] = max_length