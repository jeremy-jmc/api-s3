# Convert image to base64 string
from PIL import Image
import base64

def image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read())

image_path = './happy.png'
image_base64 = image_to_base64(image_path)
print(image_base64)