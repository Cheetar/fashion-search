import json
import pymysql
import sys, os
import numpy as np
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input

from flask import Flask

app = Flask(__name__)
 

def open_connection():
    username = os.environ["MARIADB_USERNAME"]
    password = os.environ["MARIADB_PASSWORD"]
    host = "db"
    database = os.environ["MARIADB_DATABASE"]
    cursorclass = pymysql.cursors.DictCursor
    return pymysql.connect(host, username, password, database, cursorclass = pymysql.cursors.DictCursor)

def toList(string):
    string = string.strip('[]')
    return [float(i) for i in string.split(', ')]

def distance(vector1, vector2):
    vector1 = toList(vector1)
    vector2 = toList(vector2)
    return sum(map(lambda x, y: (x-y)**2, vector1, vector2))
    
def calculate(imgpath):
    #try:    
    img = image.load_img('/img/' + imgpath, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = np.array(model.predict(img_data))
    serialized_data = features.flatten().tolist()
    return str(serialized_data)
    #except:
    #    raise Exception('Calculating failed')


@app.route('/add/<id>')
def add(id):
    #try:
    with db.cursor() as cursor:
        sql = "SELECT `image_path` FROM `images` WHERE `id`=%s"
        cursor.execute(sql, (id))
        result = cursor.fetchone()
        print(str(result['image_path']))
        vector = calculate('/img/' + str(result['image_path']))
        sql = "INSERT INTO `images` (`vector`) VALUES (%s)"
        cursor.execute(sql, (vector))
        print('Added ID:',id)
        os.remove('/img/' + str(result['image_path']))
        return 'ok', 200       
    #except:
    #    return 'error', 400

@app.route('/find/<user_img>')
def findBest(user_img):
    try:
        with db.cursor() as cursor:
            sql = "SELECT `id` `vector` FROM `images` WHERE `vector`!=NULL"
            cursor.execute(sql)            
            #user_vector = cursor.fetchone()
            distances = []            

            sql = "SELECT `id` `vector` FROM `images` WHERE `vector`!=NULL"
            cursor.execute(sql)
            result = cursor.fetchone()      
            while result != None:
                dst = distance(user_vector.vector, result.vector)
                distances.append({'id':result.id, 'distance':dst})
            
            best_distance, best_id = 10**25, -1            
            for i in distances:
                if i.distance < bestDistance:
                    best_id, best_distance = i.id, i.distance
            
            if best_id == -1:
                return 'error', 400
            else:            
                return str(best_id), 200

    except:
        return 'error', 400

@app.route('/test')    
def test():
        try:
            vector = calculate('69.jpg')
            return 'ok', 200    
        except:
            return 'error', 400


image.LOAD_TRUNCATED_IMAGES = True
model = VGG16(weights='imagenet', include_top=False)
db = open_connection()

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
