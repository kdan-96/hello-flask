import keras
import numpy as np
from keras.models import Model
from keras_vggface.vggface import VGGFace
from keras_preprocessing.image import load_img,img_to_array
from keras.applications.vgg16 import preprocess_input

#db connection
#import mysql.connector
import MySQLdb
connection = MySQLdb.connect(db="test")
mycursor = connection.cursor( )

vggface = VGGFace(model='vgg16')

vgg_face_descriptor = Model (inputs = vggface.layers[0].input , outputs = vggface.layers[-2].output)



def preprocess_image(image_path):
    img = load_img(image_path,target_size=(224,224))
    img = img_to_array(img)
    img = np.expand_dims(img,axis =0)
    img = preprocess_input(img)
    return img

def findCosDistance(src_rep,test_rep):
    a = np.matmul(np.transpose(src_rep),test_rep)
    b=np.sum(np.multiply(src_rep,src_rep))
    c= np.sum(np.multiply(test_rep,test_rep))
    cosDist =  1- (a/(np.sqrt(b)*np.sqrt(c)))
    print (cosDist)
    return cosDist

def findEucDistance(src_rep,test_rep):
    euc_dist = src_rep - test_rep
    euc_dist = np.sum(np.multiply(euc_dist,euc_dist))
    euc_dist = np.sqrt(euc_dist)
    return euc_dist


epsilon = 0.40 #cosine similarity
#epsilon = 120 #euclidean distance

def verifyFace(img1,img2):
    print('trying to verify')
    img1_rep = vgg_face_descriptor.predict(preprocess_image(img1))[0,:]
    img2_rep = vgg_face_descriptor.predict(preprocess_image(img2))[0,:]

    #print (img1_rep)
    #print (type(img1_rep))

    #numpy array to BLOB
    byte_array = img1_rep.tostring()

    #inserting into database
    query = f"INSERT INTO user_info (uid,features) VALUES (%s,%s)"
    uid=6
    args = (uid,byte_array)
    #print("args",args)
    #print (query,args)
    mycursor.execute(query,args)
    connection.commit()
    #read data from database

    readData = "SELECT uid FROM user_info"
    mycursor.execute(readData)
    myresult = mycursor.fetchall()

    for row in myresult:
        print (row)

    
    #BLOB to numpy array
    numpy_arr = np.fromstring(byte_array)
    #print (numpy_arr)

    
    cos_similarity = findCosDistance(img1_rep,img2_rep)
    if(cos_similarity < epsilon):
        print("verified... they are same person")
    else:
        print("unverified! they are not same person!")

verifyFace('F:/sem5-mine/SE_project/Tutorials/deepface-sefiks/8.jpg','F:/sem5-mine/SE_project/Tutorials/deepface-sefiks/7.jpg')





