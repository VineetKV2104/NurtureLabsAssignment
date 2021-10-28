from enum import unique
from flask import Flask,request,redirect,session,jsonify,Response,make_response
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import os
import jwt 
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import re
import json
import io
from base64 import encodebytes
from PIL import Image
from datetime import datetime,date


app = Flask(__name__)
app.config['SECRET_KEY'] = 'nutureLabsTest'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutureLabs.sqlite3'
db = SQLAlchemy(app)
 
class advisorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)

class userData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False,unique=True)
    password = db.Column(db.String(500), nullable=False)

class bookingData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.String(10), nullable=False)
    uid = db.Column(db.String(100), nullable=False)
    aid = db.Column(db.String(100), nullable=False)
    booking_time = db.Column(db.DateTime,nullable=False,unique=True)
    


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # print(token)
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 400
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
            # print(data)
            current_user = userData.query.filter_by(uid=data['User_ID']).first()
        except Exception as e:
            # print(e)
            return jsonify({'message' : 'Token is invalid!'}), 400
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/admin/advisor', methods=['POST'])
def advisor():
    try:
        if request.method == 'POST':
            advisor_count = advisorData.query.count()
            aid = 'AID'+str(advisor_count+1)
            if request.form['advisor_name'] == '':
                return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Please Fill All The Fields"}),status=400) 
            file = request.files['advisor_img']
            file.seek(0, os.SEEK_END)
            if file.tell() == 0:
                return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"No File Selected"}),status=400) 
            file.seek(0)
            advisor_name = request.form['advisor_name']
            file.save('static/images/'+aid+'_'+secure_filename(file.filename))        
            add_data = advisorData(aid=aid,name=advisor_name,image='static/images/'+aid+'_'+secure_filename(file.filename))
            db.session.add(add_data)
            db.session.commit()
            return Response(json.dumps({"status":"200_OK"}), status=200)
    except Exception as e:
        print(e)
        return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Internal Error"}),status=400) 

@app.route('/user/register',methods=['POST'])
def userRegister():
    try:
        if request.method == 'POST':
            user_data = userData.query.count()
            uid = 'UID'+str(user_data+1)
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            if name == '' or email == '' or password == '':
                return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Please Provide All fields"}),status=400)
            if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
                return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Invalid Email"}),status=400)
            hashed_password = generate_password_hash(password, method='sha256')
            add_user = userData(uid=uid,name=name,email=email,password=hashed_password)
            db.session.add(add_user)
            db.session.commit()
            user = userData.query.filter_by(uid=uid).first()
            token = jwt.encode({'User_ID' : user.uid}, app.config['SECRET_KEY'])
            return Response(json.dumps({'token' : token,'User_ID' : user.uid}),status=200)
    except Exception as e:
            print(e)
            return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Internal Error"}),status=400)   

@app.route('/user/login',methods=['POST'])
def login():
    if request.method=='POST':
        email =  request.form['email']
        password = request.form['password']
        if email == '' or password == '':       
            return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Please Provide All fields"}),status=400)
        if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
            return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Invalid Email"}),status=400)
        user = userData.query.filter_by(email=email).first()
        if not user:
            return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"User Not Found"}),status=400)
        if check_password_hash(user.password, password):
            token = jwt.encode({'User_ID' : user.uid}, app.config['SECRET_KEY'])
            return Response(json.dumps({'token' : token,'User_ID' : user.uid}),status=200)
        return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Wrong Password. Please try again."}),status=400)



@app.route('/user/<user_id>/advisor',methods=['GET'])
@token_required
def showAdvisors(current_user,user_id):
    try:
        if not current_user.uid:
            return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Login Required"}),status=400)
        user = userData.query.filter_by(uid=user_id).first() 
        if not user:
            return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"User Id Missing"}),status=400)
        response = {}
        advisor_data = advisorData.query.all()
        for a in advisor_data:
            image_path = a.image # point to your image location
            encoded_img = get_response_image(image_path)      
            temp = {a.aid:{'Advisor_ID': a.aid, 'Advisor_Name' : a.name,'Advisor_Profile_Pic': encoded_img}}
            response.update(temp)
        return Response(json.dumps(response),status=200)
    except Exception as e:
        print(e)
        return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Internal Error"}),status=400)


@app.route('/user/<user_id>/advisor/<advisor_id>/', methods=['POST'])
@token_required
def bookAdvisors(current_user,user_id,advisor_id):
    if request.method=='POST':
        try:
            booking_date = request.form['booking_date']
            format = "%d-%m-%Y"
            res = True
            today = date.today()
            today = today.strftime("%d-%m-%Y")
            today = datetime.strptime(today, format)
            booking_date_temp = datetime.strptime(booking_date, format)
            if today >= booking_date_temp:
                return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Please Enter Correct Date. Note:- Booking can only be done starting from tomorrow's date. "}),status=400)
            reserved = bookingData.query.filter_by(booking_time=booking_date_temp).first()
            if reserved != None:
                return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Date Already Reserved"}),status=400)
            try:
                res = bool(datetime.strptime(booking_date, format))
                if res:
                    booking_data = bookingData.query.count()
                    bid = 'BID'+str(booking_data+1)
                    book_date = bookingData(bid=bid,aid=advisor_id,uid=user_id,booking_time=booking_date_temp)
                    db.session.add(book_date)
                    db.session.commit()
                    return Response(json.dumps({"status":"200_OK"}), status=200)
            except  Exception as e:
                print(e)
                return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Please Enter Correct Date Format. (dd-mm-yyyy) "}),status=400)
        except Exception as e:
            print(e)
            return Response(json.dumps({"status":"400_BAD_REQUEST","Error":"Please Enter Correct Date Format. (dd-mm-yyyy) "}),status=400)


# @app.route('/user/<user-id>/advisor/booking')
# def showAdvisors(current_user,user_id):
#     return



if __name__ == '__main__':
    app.run(debug=False)