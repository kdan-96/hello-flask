#!C:\Users\User\AppData\Local\Programs\Python\Python36/python3

from flask import Flask, render_template, request
from werkzeug import secure_filename
from model_copy import verifyUploadedFace
app = Flask(__name__)


	
@app.route('/test', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      if (model_copy.verifyUploadedFace(secure_filename(f.filename))):
         return jsonify(valid=true)
      else:
         return jsonify(valid=false)
		
if __name__ == '__main__':
   app.run(debug = True)
