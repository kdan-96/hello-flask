

from flask import Flask, render_template, request,jsonify,Response
from werkzeug import secure_filename
from model_copy2 import verifyUploadedFace,preprocess_image,findCosDistance
import pprint
from PIL import Image
import os,os.path
app = Flask(__name__)
path=r"F:\sem5-mine\SE_project\Project\node_server\nodeServer\src\uploads"

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
            #img=(Image.open(os.path.join(path,python_filename))
            
      #f.save(secure_filename(f.filename))
      
      #val=verifyUploadedFace(secure_filename(f.filename))
      val=verifyUploadedFace(os.path.join(path,python_filename))
      #return jsonify(val)
      return jsonify(f)
      
      
   else:
      print ("no request")
      return jsonify(valid=False)

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
