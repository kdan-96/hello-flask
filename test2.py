

from flask import Flask, render_template, request,jsonify
from werkzeug import secure_filename
from model_copy2 import verifyUploadedFace,preprocess_image,findCosDistance
app = Flask(__name__)


print ("working")
@app.route('/test', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      print ("post req")
      f = request.files['file']
      f.save(secure_filename(f.filename))
      val=verifyUploadedFace(secure_filename(f.filename))
      return jsonify(val)
   else:
      print ("no request")
      return jsonify(valid=False)
		
if __name__ == '__main__':
   app.run(debug = True)
