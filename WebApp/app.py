import os, requests, qrcode, base64, io
from flask import Flask, render_template, request, jsonify
from PIL import Image

def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

iot_central_url_root = 'https://' + \
                       os.environ['APP_NAME'] + \
                       '.azureiotcentral.com/api/preview/devices/' + \
                       os.environ['DEVICE_NAME'] + \
                       '/components/' + \
                       os.environ['COMPONENT_NAME'] + \
                       '/commands/'

api_key = os.environ['API_KEY']

app = Flask(__name__)

# The root route, returns the home.html page
@app.route('/')
def home():
    # Add any required page data here
    page_data = {}
    return render_template('home.html', page_data = page_data)

def postCommand(command_name, request):
    headers = {'Authorization': api_key}
    requests.post(iot_central_url_root + command_name, json={'request': request}, headers=headers)

@app.route('/updateName', methods=['POST'])
def update_name():
    body = request.get_json()
    name = body['wearer_name']
    postCommand('UpdateName', name)
    return {}

@app.route('/updateLink', methods=['POST'])
def update_link():
    body = request.get_json()
    link = body['badge_link']

    img = qrcode.make(link)

    print(type(img))
    print(img.size)
    bytes = image_to_byte_array(img)
    postCommand('UpdateImage', base64.b64encode(bytes).decode())
    return {}