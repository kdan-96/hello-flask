from flask import Flask,request,redirect,url_for,flash
from flask_cors import CORS
#import model.py
#from werkzeug.utils import secure_filenname

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some secret key'



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/test',methods=['GET','POST','OPTIONS'])
def upload():
    if request.method == 'GET':
        flash('hello')
    if request.method == 'POST':
        return request.get_json(force=True)
        if 'file' not in request.files:
            flash('No file included')
            return redirect(request.url)
    image = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if image and allowed_file(file.filename):
        if file:
            #filename = secure_filename(file.filename)
            filename=file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            flash('upload successful')
            return redirect(request.url)

@app.route('/',methods=['GET','POST','OPTIONS'])
def hello_world():
    return 'Hello, World!'
