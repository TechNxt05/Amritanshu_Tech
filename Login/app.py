from cryptography.fernet import Fernet
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import random
import string
import os
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///login_details.db"
app.secret_key = 'your_secret_key'

DB_PATH = os.path.abspath('C:/Users/Amritanshu/OneDrive/Desktop/Projects/Login System/props.db')

def get_mail_config():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT Value FROM Property WHERE Key = ? AND isActive = 1', ('mail_username',))
    mail_username = cursor.fetchone()[0]
    cursor.execute('SELECT Value FROM Property WHERE Key = ? AND isActive = 1', ('mail_password',))
    mail_password = cursor.fetchone()[0]
    conn.close()
    return mail_username, mail_password

mail_username, mail_password = get_mail_config()
print(mail_username)
print(mail_password)

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password

# Generate a key for encryption/decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to encrypt a password
def encrypt_password(password):
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    return encrypted_password

# Function to decrypt a password
def decrypt_password(encrypted_password):
    decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
    return decrypted_password

mail = Mail(app)
db = SQLAlchemy(app)



class Login(db.Model):
    uno = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(200), unique=True, nullable=False)
    mainpass = db.Column(db.String(50), nullable=False)
    pass1 = db.Column(db.String(50), nullable=False)
    pass2 = db.Column(db.String(50), nullable=True)
    pass3 = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.uno} - {self.uname}"

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('login.uno'), nullable=False)

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def get_file_path(key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT VALUE FROM Property WHERE KEY = ? AND isActive = 1', (key,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        raise FileNotFoundError(f"File path for key '{key}' not found or is inactive.")

def path_check():
    keys_to_fetch = ['login', 'signin', 'verify_otp']  # Example keys you want to fetch

    for key in keys_to_fetch:
        try:
            file_path = get_file_path(key)
            print(f"File path for key '{key}': {file_path}")
        except FileNotFoundError as e:
            print(e)

@app.route('/', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['username']
        passw = request.form['password']

        existing_user = Login.query.filter_by(uname=uname).first()
        if existing_user:
            flash('Username already exists!', category='error')
            return redirect(url_for('register'))

        # Extract first name from form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        age = request.form['age']
        gender = 'Male' if request.form.get('gender') == 'dot-1' else 'Female'
        city = request.form['city']
        nationality = request.form['nationality']

        encrypted_password = encrypt_password(passw)

        log = Login(uname=uname, pass1=encrypted_password, mainpass=encrypted_password)
        db.session.add(log)
        db.session.commit()

        user_details = UserDetails(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            age=age,
            gender=gender,
            city=city,
            nationality=nationality,
            user_id=log.uno
        )
        db.session.add(user_details)
        db.session.commit()

        flash('Registered successfully!', category='success')
        return redirect(url_for('login'))

    return render_template(get_file_path('login'))

@app.route('/signin', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Please enter both username and password', 'error')
            return redirect(url_for('login'))

        user = Login.query.filter_by(uname=username).first()

        if user is None:
            flash('Username does not exist', 'error')
        else:
            password_age = datetime.utcnow() - user.date
            decrypted_password = decrypt_password(user.mainpass)

            if password_age.days > 60:
                user.mainpass = ''
                db.session.commit()
                flash('Your Password has expired. Reset Your Password by going to "Forgot Password"', 'error')
            elif decrypted_password != password:
                flash('Wrong password', 'error')
            else:
                flash('Login successful', 'success')
                return redirect(url_for('home_page'))  # Redirect to home page upon successful login

    return render_template(get_file_path('signin'))

@app.route('/home')
def home_page():
    return render_template(get_file_path('home'))

@app.route('/otp', methods=["GET", "POST"])
def otp_page():
    if request.method == "POST":
        email = request.form.get('email')

        # Check if the email exists in UserDetails table
        user_details = UserDetails.query.filter_by(email=email).first()

        if user_details:
            otp = generate_otp()
            session['otp'] = otp
            session['email'] = email
            
            msg = Message('Your OTP Code', sender='amritanshu05yadav@gmail.com', recipients=[email])
            msg.body = f'Your OTP code is {otp}'
            mail.send(msg)
            
            flash('OTP sent to your email address', 'info')
            return redirect(url_for('verify_otp'))
        else:
            flash('Email not found in our records', 'error')
    return render_template(get_file_path('OTP'))

@app.route('/verify_otp', methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        entered_otp = request.form.get('otp')
        if entered_otp == session.get('otp'):
            return redirect(url_for('reset_page'))
        else:
            flash('Wrong OTP', 'error')
    return render_template(get_file_path('verify_otp'))

@app.route('/reset', methods=["GET", "POST"])
def reset_page():
    if request.method == "POST":
        new_password = request.form.get('new_password')
        email = session.get('email')
        
        user_details = UserDetails.query.filter_by(email=email).first()

        if user_details:
            user = Login.query.get(user_details.user_id)

            # Encrypt the new password
            encrypted_new_password = encrypt_password(new_password)

            # Check if the new password is the same as any of the previous passwords
            if encrypted_new_password in [user.mainpass, user.pass1, user.pass2, user.pass3]:
                flash('New password cannot be the same as any of the previous passwords.', 'error')
            else:
                # Shift passwords and update with the new one
                user.pass3 = user.pass2
                user.pass2 = user.pass1
                user.pass1 = encrypted_new_password
                user.mainpass = encrypted_new_password
                user.date = datetime.utcnow()
                
                db.session.commit()
                flash('Password updated successfully.', 'success')
                return redirect(url_for('login'))
        else:
            flash('User not found.', 'error')

    return render_template(get_file_path('reset'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print("Starting Flask app...")
    path_check()
    app.run(debug=False, port=9000)
