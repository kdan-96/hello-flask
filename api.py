

from flask import Flask, render_template, request,jsonify,Response
from werkzeug import secure_filename
from model import verifyUploadedFace,preprocess_image,findCosDistance,verifyFaceComparedToRegisteredFace
import pprint
from PIL import Image
import os,os.path
from json_tricks import  dumps,  loads

app = Flask(__name__)
path=r"/home/kalana_16/uploads"
registerPath=r"/home/kalana_16/register"




'''- When a user is registered an API call is sent to node server about user details
   -Node server generate another API call uid and photo of the user to the flask server to preprocess
   -After preprocessing,the vector is returned to node server with the uid
   -relevant userID is taken from email and face vector is saved to database
'''
#This end point is called when registering a user 
@app.route('/preprocess',methods = ['POST'])
#File upload handler
def preprocess():
      if request.method=='POST':
            print ("preprocess request recieved")
            f = request.get_json(force=True)
            filename =f['filename']
            print (filename)
            for python_filename in os.listdir(registerPath):
                  print (python_filename)
                  if python_filename==filename:
                     print ('file found under register directory')  
                  else:
                     print('file missing under register directory')
		            
#File saved to location defined under upload folder
            vector=preprocess_image(os.path.join(registerPath,python_filename))
            print (vector)
            return dumps(vector)

'''
- When a face needs verification,image of the face is sent to the node server along with the uid
- Preprocessed face vector for that uid is taken from the database and that is sent to flask server with the current image name
- flask server will compare the images and send the similarity value
'''
#This endpoint is called when verifying a user

@app.route('/verify', methods = ['GET', 'POST'])
def verify():
   print ("verification request recieved")
   if request.method == 'POST':
      f = request.get_json(force=True)
      filename =f['filename']
      print (filename)
      print (path)
      registeredImg = f['face_vector']
      
      registeredImg = loads(registeredImg,conv_str_byte=True)
      for python_filename in os.listdir(path):
         if python_filename==filename:
            print ('file found')
         else:
            print('file not found')
            
      val=verifyFaceComparedToRegisteredFace(registeredImg,os.path.join(path,filename))
      print (os.path.join(path,filename))
      os.remove(os.path.join(path,filename))
      return jsonify(val)
      
   else:
      print ("no request")
      return jsonify(valid=False)


@app.route('/',methods = ['GET','POST']) 
def root():
   if request.method=='GET':
      print ("root running")
      return jsonify(get=True)
   if request.method=='POST':
      print ('recieved a request')
      print(request.json)





'''
- File name is sent to endpoint
- File location is defined in the path variable
- Read the file using file name from the location and calculate the similarity
'''

print ("working")
@app.route('/test', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.get_json(force=True)
      filename =f['filename']
      print(filename)
      return jsonify(valid=True)
      
      
   else:
      print ("no request")
      return jsonify(valid=False)


		
if __name__ == '__main__':
   app.run(debug = True)
