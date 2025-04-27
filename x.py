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
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB - size in bytes
MAX_FILES = 5

def validate_item_images():
    images_names = []
    if "files" not in request.files:
        raise Exception("company_ex at least one file")
    
    files = request.files.getlist('files')
    
    # TODO: Fix the validation for 0 files
    # if not files == [None]:
    #     raise Exception("company_ex at least one file")  
    
    if len(files) > MAX_FILES:
        raise Exception("company_ex max 5 files")

    for the_file in files:
        file_size = len(the_file.read()) # size is in bytes                 
        file_name, file_extension = os.path.splitext(the_file.filename)
        the_file.seek(0)
        file_extension = file_extension.lstrip(".")
        if file_extension not in ALLOWED_EXTENSIONS:
            raise Exception("company_ex file extension not allowed")  
        if file_size > MAX_FILE_SIZE:
            raise Exception("company_ex file too large")  
        new_file_name = f"{uuid.uuid4().hex}.{file_extension}"
        images_names.append(new_file_name)
        file_path = os.path.join("static/uploads", new_file_name)
        the_file.save(file_path) 
    return images_names


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
def send_email(user_name, user_last_name):
    try:
        # Create a gmail
        # Enable (turn on) 2 step verification/factor in the google account manager
        # Visit: https://myaccount.google.com/apppasswords

        # Email and password of the sender's Gmail account
        sender_email = ""
        password = ""  # If 2FA is on, use an App Password instead

        # Receiver email address
        receiver_email = ""
        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = "My company name"
        message["To"] = ""
        message["Subject"] = "Welcome"

        # Body of the email
        body = f"Thank you {user_name} {user_last_name} for signing up. Welcome."
        # body = f"""To verify your account, please <a href="http://127.0.0.1/verify/{user_verification_key}">click here</a>"""
        message.attach(MIMEText(body, "html"))

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        ic("Email sent successfully!")

        return "email sent"

    except Exception as ex:
        ic(ex)
        raise Exception("cannot send email")
    finally:
        pass





