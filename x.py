from flask import request, session
import mysql.connector
import re
import os
import uuid

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)


##############################
def db():
    db = mysql.connector.connect(
        host = "mysql",      # Replace with your MySQL server's address or docker service name "mysql"
        user = "root",  # Replace with your MySQL username
        password = "password",  # Replace with your MySQL password
        database = "company"   # Replace with your MySQL database name
    )
    cursor = db.cursor(dictionary=True)
    return db, cursor


##############################
def validate_user_logged():
    if not session.get("user"): raise Exception("compay_ex user not logged")
    return session.get("user")



##############################
USER_NAME_MIN = 2
USER_NAME_MAX = 30
USER_NAME_REGEX = f"^.{{{USER_NAME_MIN},{USER_NAME_MAX}}}$"
def validate_user_name():
    error = "company_ex user_name"
    user_name = request.form.get("user_name", "").strip()
    if not re.match(USER_NAME_REGEX, user_name): raise Exception(error)
    return user_name


##############################
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 30
USER_LAST_NAME_REGEX = f"^.{{{USER_LAST_NAME_MIN},{USER_LAST_NAME_MAX}}}$"
def validate_user_last_name():
    error = "company_ex user_last_name"
    user_last_name = request.form.get("user_last_name", "").strip()
    if not re.match(USER_LAST_NAME_REGEX, user_last_name): raise Exception(error)
    return user_last_name


##############################
USER_USERNAME_MIN = 3
USER_USERNAME_MAX = 30
USER_USERNAME_REGEX = f"^[a-zA-Z0-9_]{{{USER_USERNAME_MIN},{USER_USERNAME_MAX}}}$"
def validate_user_username():
    error = "company_ex user_username"
    user_username = request.form.get("user_username", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_username): raise Exception(error)
    return user_username


##############################
REGEX_PAGE_NUMBER = "^[1-9][0-9]*$"
def validate_page_number(page_number):
    error = "company_ex page number"
    page_number = page_number.strip()
    if not re.match(REGEX_PAGE_NUMBER, page_number): raise Exception(error)
    return int(page_number)


##############################
USER_EMAIL_REGEX = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
def validate_user_email():
    error = f"company_ex user_email"
    user_email = request.form.get("user_email", "").strip()
    if not re.match(USER_EMAIL_REGEX, user_email): raise Exception(error)
    return user_email


##############################
USER_PASSWORD_MIN = 8
USER_PASSWORD_MAX = 64
USER_PASSWORD_REGEX = f"^.{{{USER_PASSWORD_MIN},{USER_PASSWORD_MAX}}}$"
def validate_user_password():
    error = "company_ex user_password"
    user_password = request.form.get("user_password", "").strip()
    if not re.match(USER_PASSWORD_REGEX, user_password): raise Exception(error)
    return user_password


##############################
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
MAX_FILE_SIZE = 5 * 1024 * 1024 
MAX_FILES = 3


###############################
def validate_item_images():    
    images_names = []
    if "files" not in request.files:
        return []
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        return []
    
    if len(files) > MAX_FILES:
        raise Exception(f"Maximum {MAX_FILES} images allowed")

    for the_file in files:
        file_size = len(the_file.read())  # size is in bytes                 
        the_file.seek(0)
        
        file_name, file_extension = os.path.splitext(the_file.filename)
        file_extension = file_extension.lstrip(".").lower()
        
        if file_extension not in ALLOWED_EXTENSIONS:
            raise Exception("File extension not allowed")
            
        if file_size > MAX_FILE_SIZE:
            raise Exception("File too large")
            
        new_file_name = f"{uuid.uuid4().hex}.{file_extension}"
        images_names.append(new_file_name)
        
        file_path = os.path.join("static/uploads", new_file_name)
        the_file.save(file_path)
        
    return images_names


###############################
def get_additional_images(item_pk):
    """Get all additional images for a fleamarket item"""
    db_conn, cursor = db()
    try:
        q = "SELECT image_name FROM images WHERE image_item_fk = %s"
        cursor.execute(q, (item_pk,))
        return [row['image_name'] for row in cursor.fetchall()]
    finally:
        cursor.close()
        db_conn.close()


##############################
ITEM_NAME_MIN = 2
ITEM_NAME_MAX = 20
ITEM_NAME_REGEX = f"^.{{{ITEM_NAME_MIN},{ITEM_NAME_MAX}}}$"
def validate_item_name():
    error = f"itemname {ITEM_NAME_MIN} to {ITEM_NAME_MAX} characters"
    item_name = request.form.get("item_name", "").strip()
    if not re.match(ITEM_NAME_REGEX, item_name): raise Exception(error)
    return item_name


##############################
ITEM_ADDRESS_MIN = 5
ITEM_ADDRESS_MAX = 100
ITEM_ADDRESS_REGEX = f"^.{{{ITEM_ADDRESS_MIN},{ITEM_ADDRESS_MAX}}}$"
def validate_item_address():
    error = f"address {ITEM_ADDRESS_MIN} to {ITEM_ADDRESS_MAX} characters"
    item_address = request.form.get("item_address", "").strip()
    if not re.match(ITEM_ADDRESS_REGEX, item_address): raise Exception(error)
    return item_address


##############################
ITEM_IMAGE_REGEX = r"^[a-zA-Z0-9_-]+\.(jpg|jpeg|png|gif|webp)$"
def validate_item_image():
    error = "Invalid image format (use jpg, jpeg, png, gif, or webp)"
    item_image = request.form.get("item_image", "").strip()
    if not re.match(ITEM_IMAGE_REGEX, item_image): raise Exception(error)
    return item_image


##############################
ITEM_PRICE_MIN = 0
ITEM_PRICE_MAX = 65535
ITEM_PRICE_REGEX = f"^([0-9]{{1,3}}(,[0-9]{{3}})*|[0-9]+)(\.[0-9]{{1,2}})?$"
def validate_item_price():
    error = f"item price {ITEM_PRICE_MIN} to {ITEM_PRICE_MAX} characters"
    item_price = request.form.get("item_price", "").strip()
    if not re.match(ITEM_PRICE_REGEX, item_price): raise Exception(error)
    item_price = item_price.replace(",", "")
    if not (ITEM_PRICE_MIN <= float(item_price) <= ITEM_PRICE_MAX): raise Exception(error)
    return item_price


##############################
# Latitude must be between -90 and 90
ITEM_LATITUDE_REGEX = r"^-?([0-8]?[0-9]|90)(\.[0-9]{1,6})?$"
def validate_item_latitude():  # Note: function name has a typo in app.py
    error = "Latitude must be between -90 and 90"
    item_latitude = request.form.get("item_latitude", "").strip()
    if not re.match(ITEM_LATITUDE_REGEX, item_latitude): raise Exception(error)
    return item_latitude


##############################
# Longitude must be between -180 and 180
ITEM_LONGITUDE_REGEX = r"^-?((1?[0-7]?|[0-9]?)[0-9]|180)(\.[0-9]{1,6})?$"
def validate_item_longitude():
    error = "Longitude must be between -180 and 180"
    item_longitude = request.form.get("item_longitude", "").strip()
    if not re.match(ITEM_LONGITUDE_REGEX, item_longitude): raise Exception(error)
    return item_longitude


##############################
def send_email_notification(recipient_email, subject, body, user_name="", user_lastname=""):
    """
    Centralized email sending function
    
    Parameters:
    - recipient_email: The email address of the recipient
    - subject: Email subject line
    - body: HTML content of the email
    - user_name: Optional user's first name
    - user_lastname: Optional user's last name
    """
    try:
        # Email credentials - centralized in one place
        sender_email = "lindehojpizza@gmail.com"
        password = "dfca sgvy uwwy brjx"  # App password
        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = "Fleamarket App"
        message["To"] = recipient_email
        message["Subject"] = subject
        
        # Attach the HTML body
        message.attach(MIMEText(body, "html"))
        
        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        ic(f"Email sent successfully: {subject}")
        return True
        
    except Exception as ex:
        ic(ex)
        raise Exception(f"Cannot send email: {str(ex)}")

def send_verification_email(user_name, user_lastname, verification_key, recipient_email):
    """Send account verification email"""
    subject = "Verify Your Fleamarket Account"
    body = f"""
    <p>Thank you {user_name} {user_lastname} for signing up to Fleamarket.</p>
    <p>Please click here to verify your account:
    <a href="http://127.0.0.1/verify/{verification_key}">Verify Account</a>
    </p>
    """
    return send_email_notification(recipient_email, subject, body, user_name, user_lastname)

def send_password_reset_email(user_name, user_lastname, reset_key, recipient_email):
    """Send password reset email"""
    subject = "Reset Your Fleamarket Password"
    body = f"""
    <p>Hello {user_name} {user_lastname},</p>
    <p>We received a request to reset your password. Click the link below to create a new password:</p>
    <p><a href="http://127.0.0.1/reset-password/{reset_key}">Reset Password</a></p>
    <p>This link will expire in 1 hour.</p>
    <p>If you did not request a password reset, you can ignore this email.</p>
    """
    return send_email_notification(recipient_email, subject, body, user_name, user_lastname)

def send_account_deletion_email(user_name, user_lastname, recipient_email):
    """Send account deletion notification email"""
    subject = "Account Deletion Confirmation"
    body = "<p>Your profile has been deleted.</p>"
    return send_email_notification(recipient_email, subject, body, user_name, user_lastname)

def send_user_blocked_email(user_name, user_lastname, recipient_email):
    """Send notification when a user is blocked"""
    subject = "Your Fleamarket Account Has Been Blocked"
    body = f"""
    <p>Hello {user_name} {user_lastname},</p>
    <p>We regret to inform you that your Fleamarket account has been blocked by an administrator.</p>
    <p>If you believe this is an error or have questions, please contact our support team.</p>
    """
    return send_email_notification(recipient_email, subject, body, user_name, user_lastname)

def send_item_blocked_email(user_name, user_lastname, item_name, recipient_email):
    """Send notification when a user's fleamarket is blocked"""
    subject = "Your Fleamarket Listing Has Been Blocked"
    body = f"""
    <p>Hello {user_name} {user_lastname},</p>
    <p>We regret to inform you that your fleamarket listing "{item_name}" has been blocked by an administrator.</p>
    <p>If you believe this is an error or have questions, please contact our support team.</p>
    """
    return send_email_notification(recipient_email, subject, body, user_name, user_lastname)


##############################
def user_verification_key():
    """Generate a unique verification key"""
    return str(uuid.uuid4())





