# wahyu zuhudistia khoiri 19090129 (6a)
# rian pratama (19090069) (6d)


from lib2to3.pgen2 import token
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense,Conv2D,MaxPool2D,Dropout,BatchNormalization,Flatten,Activation
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from keras.utils.vis_utils import plot_model
import pickle
from flask import Flask, jsonify,request,flash,redirect,render_template, session,url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from itsdangerous import json
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from flask_restful import Resource, Api
import pymongo
from pymongo import MongoClient
import re
import hashlib
from flask_ngrok import run_with_ngrok
import datetime

app = Flask(__name__)

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'bigtuing'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)


UPLOAD_FOLDER = 'foto_prodak'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "bigtuing"

MONGO_ADDR = 'mongodb://localhost:27017'
MONGO_DB = "db_prodak"

conn = pymongo.MongoClient(MONGO_ADDR)
db = conn[MONGO_DB]
users_collection = db["admin"]

api = Api(app)
CORS(app)


from tensorflow.keras.models import load_model
MODEL_PATH = 'model.h5'
model = load_model(MODEL_PATH,compile=False)

pickle_inn = open('num_class_prodak.pkl','rb')
num_classes_prodak = pickle.load(pickle_inn)


@app.route("/api/v1/users", methods=["POST"])
def register():
	new_user = request.get_json()
	new_user["Password"] = new_user["Password"]
	doc = users_collection.find_one({"Username": new_user["Username"]})
	if not doc:
		users_collection.insert_one(new_user)
		return jsonify({'msg': 'User Admin berhasil dibuat'}), 201
	else:
		return jsonify({'msg': 'Username sudah pernah dibuat'}), 409
	return jsonify({'msg': 'Username atau Password Salah'}), 401

@app.route("/api/v1/login", methods=["POST"])
def loginApi():
	login_details = request.get_json()
	user_from_db = users_collection.find_one({'Username': login_details['Username']})

	if user_from_db:
		password = login_details['Password']
		if password == user_from_db['Password']:
			access_token = create_access_token(identity=user_from_db['Username'])
			return jsonify(access_token=access_token), 200

@app.route("/api/v1/user", methods=["GET"])
@jwt_required()
def profile():
	current_user = get_jwt_identity()
	user_from_db = users_collection.find_one({'Username' : current_user})
	if user_from_db:
		del user_from_db['_id'], user_from_db['Password']
		return jsonify({'profile' : user_from_db }), 200
	else:
		return jsonify({'msg': 'Profil admin tidak ditemukan'}), 404





def allowed_file(filename):     
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class index(Resource):
  def post(self):

    if 'image' not in request.files:
      flash('No file part')
      return jsonify({
            "pesan":"tidak ada form image"
          })
    file = request.files['image']
    if file.filename == '':
      return jsonify({
            "pesan":"tidak ada file image yang dipilih"
          })
    if file and allowed_file(file.filename):

      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      path=("foto_prodak/"+filename)

      #def predict(dir):
      img=keras.utils.load_img(path,target_size=(224,224))
      img1=keras.utils.img_to_array(img)
      img1=img1/255
      img1=np.expand_dims(img1,[0])
      plt.imshow(img)
      predict=model.predict(img1)
      classes=np.argmax(predict,axis=1)
      for key,values in num_classes_prodak.items():
          if classes==values:
            accuracy = float(round(np.max(model.predict(img1))*100,2))
            info = db['barang'].find_one({'nama': str(key)})

            if accuracy >70:
              print("The predicted image of the prodaks is: "+str(key)+" with a probability of "+str(accuracy)+"%")

              db.riwayat.insert_one({'nama_file': filename, 'path': path, 'prediksi':str(key), 'akurasi':accuracy})
            
              return jsonify({
                "barang":str(key),
                "harga" : info['harga'],
                "Accuracy":str(accuracy)+"%"      
              })
            else :    
              print("The predicted image of the prodak is: "+str(key)+" with a probability of "+str(accuracy)+"%")
              return jsonify({
                "Message":str("Jenis Barang belum tersedia "),
                "Accuracy":str(accuracy)+"%"               
                
              })
      
    else:
      return jsonify({
        "Message":"bukan file image"
      })

@app.route('/admin')
def admin():
    return render_template("login.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        Username = request.form['Username']
        Password = request.form['Password'] # .encode('utf-8')
        user = db['admin'].find_one({'Username': str(Username)})
        print(user)

        if user is not None and len(user) > 0:
            if Password == user['Password']:
                
                session['Username'] = user['Username']
                return redirect(url_for('prodak'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
    
    return render_template('dashboard.html')
#menampilkan  daftar tamu
@app.route('/prodak')
def prodak():
    data = db['barang'].find({})
    print(data)
    return render_template('prodak.html',barang  = data)

@app.route('/riwayat')
def riwayat():
    dataRiwayat = db['riwayat'].find({})
    print(dataRiwayat)
    return render_template('riwayat.html',riwayat  = dataRiwayat)

@app.route('/tambahData')
def tambahData():

    return render_template('tambahData.html')
#roses memasukan data Barang ke database
@app.route('/daftarIkan', methods=["POST"])
def daftarIkan():
    if request.method == "POST":
        barang = request.form['barang']
        harga = request.form['harga']
        if not re.match(r'[A-Za-z]+', barang):
            flash("Nama harus pakai huruf Dong!")
        
        else:
            db.ikan.insert_one({'nama': barang,'harga':harga})
            flash('Data Barang berhasil ditambah')
            return redirect(url_for('barang'))

    return render_template("tambahData.html")

@app.route('/editbarang/<nama>', methods = ['POST', 'GET'])
def editbarang(barang):
  
    data = db['barang'].find_one({'barang': barang})
    print(data)
    return render_template('editBarang.html', editBarang = data)

#melakukan roses edit data
@app.route('/updateBarng/<nama>', methods=['POST'])
def updatBarang(barang):
    if request.method == 'POST':
        barang = request.form['barang']
        harga = request.form['harga']
        if not re.match(r'[A-Za-z]+', barang):
            flash("Nama harus pakai huruf Dong!")
        else:
          db.barang.update_one({'barang': barang}, 
          {"$set": {
            'barang': barang,  
            'harga': harga
            }
            })

          flash('Data Barang berhasil diupdate')
          return render_template("popUpEdit.html")

    return render_template("prodak.html")

#menghaus daftar Burung
@app.route('/hapusBarang/<nama>', methods = ['POST','GET'])
def hapusBarang(nama):
  
    db.data_burung.delete_one({'barang': nama})
    flash('Burung barang Dihapus!')
    return redirect(url_for('barang'))

@app.route('/hapusRiwayat/<nama_file>', methods = ['POST','GET'])
def hapusRiwayat(nama_file):
  
    db.riwayat.delete_one({'nama_file': nama_file})
    flash('Riwayat Berhasil Dihapus!')
    return redirect(url_for('riwayat'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


api.add_resource(index, "/api/image", methods=["POST"])

if __name__ == '__main__':
  

  app.run()
  app.run(debug = True, port=5000, host='0.0.0.0')

