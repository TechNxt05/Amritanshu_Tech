# Login System

Visit : http://localhost/

# Programming Languages :
1.	Python Flask
2.	HTML
3.	CSS
4.	Javascript
# Database : 
SQLite Database – login_details.db with 2 tables, one for storing Login details, and the other for storing User  details.
# Features :
Registration Page (login.html) - User will have to register themselves by entering their personal details and by setting up their Login Details i.e. unique Username, strong Password and Security Questions.
Sign-in Page (sigin.html) – User will have to enter their correct Login Details to sign to open their Home Page (home.html).
Reset Password Page (reset.html) – When the user clicks “Forgot Password”, OTP Verification Page (otp.html and verify_otp.html) opens where user enters his registered E-mail ID to get the OTP which is entered by the user for verification. After Verification of OTP, Reset Password Page open where the user resets his new password, which cannot be same as the previous 3 passwords.
Note : For better security, Passwords are stored in encrypted form and passwords expire after 60 days of the setting up of the password.

# Usage :
1.	Open the Terminal in a new Folder and clone this repository to your local machine.
2.	Setup a virtual environment and install the required dependencies using pip install -r requirements.txt.
3.	Run the project using python GUI.py.

# Description :
1.	Flask application app.py for back-end.
2.	The templates folder contains all html files.
3.	The static folder contains all css and javascript files.
4.	Functions –
•	register() : To store all the login details and user details in the database.
•	login() : To login by entering correct login details.
•	home_page() : To redirect to Home Page.
•	otp_page() : To redirect to OTP Page
•	generate_otp() : To send OTP on the entered email.
•	verify_otp() : To verify the OTP entered by the user with the OTP sent on the e-mail.
•	encrypt_password() : Function to encrypt the passwords and return the encrypted passwords.
•	decrypt_password() : Function to decrypt the passwords and return the decrypted passwords.
5.	Modules –
a)	Flask : Web Framework to develop web applications.
b)	Flask_sqlalchemy : Used to connect to the database.
c)	Flask-Mail : Flask extension used to send email.
d)	Date-time : Used to date of creation of password.
e)	Random : Used to generate OTP by generating random 6 digit numbers.
Cryptography-fernet : A module that provides symmetric encryption and decryption using the Fernet protocol.

# Flow Chart :
![Login2](https://github.com/TechNxt05/Amritanshu_Tech/assets/99065174/e6c28024-0b87-480c-941d-ee7f9194e1f8)

# System Architecture :
![Login3](https://github.com/TechNxt05/Amritanshu_Tech/assets/99065174/87c2e59d-3c03-4e23-8db9-129ff31cb610)



