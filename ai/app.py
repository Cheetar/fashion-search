import json
import zlib
import sys, os
import numpy as np
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input

image.LOAD_TRUNCATED_IMAGES = True
model = VGG16(weights='imagenet', include_top=False)

from flask import Flask

app = Flask(__name__)

img_stack = []

@app.route('/add/<img>')
def add(img):
	img_stack.append(img)


@app.route('/calculate/<imgpath>')
def calculate(imgpath):
	img = image.load_img('img/' + imgpath, target_size=(224, 224))
	img_data = image.img_to_array(img)
	img_data = np.expand_dims(img_data, axis=0)
	img_data = preprocess_input(img_data)
	features = np.array(model.predict(img_data))
	return zlib.compress((str(features.flatten().tolist())).encode('utf-8'))
    
    
'''
image.LOAD_TRUNCATED_IMAGES = True
model = VGG16(weights='imagenet', include_top=False)

filelist = ['img/1.jpg', 'img/2.jpg']
featurelist = []
print(filelist)
for i, imagepath in enumerate(filelist):
	print(f"Extracting features... {i}/{len(filelist)} {imagepath}")
	img = image.load_img(imagepath, target_size=(224, 224))
	img_data = image.img_to_array(img)
	img_data = np.expand_dims(img_data, axis=0)
	img_data = preprocess_input(img_data)
	features = np.array(model.predict(img_data))
	print(features)
	featurelist.append(features.flatten())
    
'''
