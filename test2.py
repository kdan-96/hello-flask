

from flask import Flask, render_template, request,jsonify,Response
from werkzeug import secure_filename
from model_copy2 import verifyUploadedFace,preprocess_image,findCosDistance
import pprint
from PIL import Image
import os,os.path
from json_tricks import dump, dumps, load, loads, strip_comments

app = Flask(__name__)
path=r"F:\sem5-mine\SE_project\Project\node_server\nodeServer\src\uploads"
registerPath=r"F:\sem5-mine\SE_project\Project\node_server\nodeServer\src\register"



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
      print (f['originalname'])
      print ("testing")
      
      for python_filename in os.listdir(path):
         if python_filename==filename:
            print ('file found')
            
      val=verifyUploadedFace(os.path.join(path,python_filename))
      #return jsonify(val)
      return jsonify(f)
      
      
   else:
      print ("no request")
      return jsonify(valid=False)


'''- When a user is registered an API call is sent to node server about user details
   -Node server generate another API call uid and photo of the user to the flask server to preprocess
   -After preprocessing,the vector is returned to node server with the uid
   -relevant userID is taken from email and face vector is saved to database
'''

@app.route('/preprocess',methods = ['POST'])
#File upload handler
def preprocess():
      if request.method=='POST':
            print ("preprocess request recieved")
            f = request.get_json(force=True)
            filename =f['filename']
            print (filename)
            for python_filename in os.listdir(registerPath):
                  if python_filename==filename:
                        print ('file found under register directory')   
#File saved to location defined under upload folder
            vector=preprocess_image(os.path.join(registerPath,python_filename))
            print (vector)
            return dumps(vector)
      


@app.route('/', methods = ['GET', 'POST'])
def test():
   if request.method=='GET':
      print ("root running")
      return jsonify(get=True)
   if request.method=='POST':
      print ('recieved a request')
      print(request.json)

      req = request.get_json()
      return jsonify(req)
      #return jsonify(request.values)
		
if __name__ == '__main__':
   app.run(debug = True)
