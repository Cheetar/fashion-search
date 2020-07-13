import pymysql
import sys, os
import numpy as np
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input

from flask import Flask

app = Flask(__name__)



image.LOAD_TRUNCATED_IMAGES = True
model = VGG16(weights='imagenet', include_top=False)
#db = open_connection()
    

def open_connection():
    username = "dbuser"
    password = 'dbuser' #os.environ["MARIADB_ROOT_PASSWORD"]
    host = "db"
    database = "testdb"
    return pymysql.connect(host, username, password, database)

def toList(string):
    string = string.strip('[]')
    return [float(i) for i in string.split(', ')]

def distance(vector1, vector2):
    return sum(map(lambda x, y: (x-y)**2, vector1, vector2))
    
def calculate(imgpath):
    try:    
        img = image.load_img('img/' + imgpath, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        features = np.array(model.predict(img_data))
        serialized_data = features.flatten().tolist()
        return str(serialized_data)
    except:
        raise Exception('Calculating failed')


@app.route('/add/<id>')    
def add(id):
    with db.cursor() as cursor:
        sql = "SELECT `image_path` FROM `images` WHERE `id`=%s"
        cursor.execute(sql, (id))
        result = cursor.fetchone()
        #return str(result)
        
        try:
            vector = calculate(result.image_path)
            sql = "INSERT INTO `images` (`vector`) VALUES (%s)"
            cursor.execute(sql, (vector))
            return('ok')       
        except:
            return('error')

@app.route('/test')    
def test():
        try:
            vector = calculate('69.jpg')
            return 'ok', 200    
        except:
            return 'error', 400


#if __name__ == "__main__":
#    main()

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
