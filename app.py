from flask import Flask, render_template, session, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
import x
import languages
import time
import uuid
import os
import redis
import re
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

##############################
@app.after_request
def disable_cache(response):
    """
    This function automatically disables caching for all responses.
    It is applied after every request to the server.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


###############################
@app.context_processor
def inject_language():
    """Make language setting available to all templates"""
    lan = session.get("language", "en")
    return dict(lan=lan, languages=languages)

@app.get("/set-language/<language>")
def set_language(language):
    try:
        languages_allowed = ["en", "dk"]
        if language not in languages_allowed: language = "en"
        
        # Store language preference in session
        session["language"] = language
        
        # Return to previous page or homepage
        referer = request.referrer or "/"
        
        return f"""
        <mixhtml mix-redirect="{referer}">
        </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return redirect(url_for("view_index"))


##############################
@app.get("/")
def view_index():
    try:
        # Get language from session or default
        lan = session.get("language", "en")
        
        db, cursor = x.db()
        q = """SELECT i.* FROM items i
        JOIN users u ON i.item_user_fk = u.user_pk
        WHERE i.item_deleted_at = 0 AND i.item_blocked_at = 0 
        AND u.user_blocked_at = 0
        ORDER BY i.item_created_at LIMIT 2"""
        cursor.execute(q)
        items = cursor.fetchall()
        return render_template("view_index.html", title="Fleamarket | Home", items=items, lan=lan, languages=languages)
    except Exception as ex:
        ic(ex)
        return redirect(url_for("view_login", error_message="System error"))
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/items/<item_pk>")
def get_item_by_pk(item_pk):
    try:
        db, cursor = x.db()
        
        # Get main item details
        q = "SELECT * FROM items WHERE item_pk = %s AND item_deleted_at = 0"
        cursor.execute(q, (item_pk,))
        item = cursor.fetchone()
        
        if not item:
            return """
                <mixhtml mix-top="body">
                    Item not found
                </mixhtml>
            """
            
        # Get additional images
        additional_images = []
        q_images = "SELECT image_name FROM images WHERE image_item_fk = %s"
        cursor.execute(q_images, (item_pk,))
        additional_images = [row['image_name'] for row in cursor.fetchall()]
        
        # Render template with both item and additional images
        html_item = render_template("_item.html", item=item, additional_images=additional_images)
        
        return f"""
            <mixhtml mix-replace="#item">
                {html_item}
            </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return """
            <mixhtml mix-top="body">
                Error loading item
            </mixhtml>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/items/page/<page_number>")
def get_items_by_page(page_number):
    try:
        page_number = x.validate_page_number(page_number)
        items_per_page = 2
        offset = (page_number-1) * items_per_page
        extra_item = items_per_page + 1
        db, cursor = x.db()
        q = """SELECT i.* FROM items i
        JOIN users u ON i.item_user_fk = u.user_pk
        WHERE i.item_deleted_at = 0 AND i.item_blocked_at = 0 
        AND u.user_blocked_at = 0
        ORDER BY i.item_created_at LIMIT %s OFFSET %s"""
        cursor.execute(q, (extra_item, offset))
        items = cursor.fetchall()
        html = ""
        # return "x"
        for item in items[:items_per_page]:
            i = render_template("_item_mini.html", item=item)
            html += i
        button = render_template("_button_more_items.html", page_number=page_number + 1)
        if len(items) < extra_item: button = ""
        return f"""
            <mixhtml mix-bottom="#items">
                {html}
            </mixhtml>
            <mixhtml mix-replace="#button_more_items">
                {button}
            </mixhtml>
            <mixhtml mix-function="add_markers_to_map">
                {json.dumps(items[:items_per_page])}
            </mixhtml>            
        """
    except Exception as ex:
        ic(ex)
        if "company_ex page number" in str(ex):
            return """
                <mixhtml mix-top="body">
                    page number invalid
                </mixhtml>
            """
        return """
            <mixhtml mix-top="body">
                ups
            </mixhtml>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/signup")
def view_signup():
    try:
        lan = session.get("language", "en")
        return render_template("view_signup.html", title="Fleamarket | Signup", x=x, lan=lan, languages=languages)
    except Exception as ex:
        ic(ex)
    finally:
        pass


##############################
@app.post("/signup")
def signup():
    try:
        lan = session.get("language", "en")

        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        user_username = x.validate_user_username()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        hashed_password = generate_password_hash(user_password)
        user_created_at = int(time.time())
        user_pk = uuid.uuid4().hex  # Generate UUID for primary key
        verification_key = uuid.uuid4().hex  # Generate verification key

        q = """INSERT INTO users 
        (user_pk, user_username, user_name, user_last_name, user_email, 
        user_password, user_verification_key, user_created_at, user_updated_at, user_deleted_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        db, cursor = x.db()
        cursor.execute(q, (user_pk, user_username, user_name, user_last_name, 
                        user_email, hashed_password, verification_key, user_created_at, 0, 0))

        if cursor.rowcount != 1: raise Exception("System under maintenance")

        db.commit()
        x.send_verification_email(user_name, user_last_name, verification_key, user_email)
        return redirect(url_for("view_login", message="Signup successful! Please check your email to verify your account before logging in."))
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        
        
        if "username" in str(ex):
            return render_template("view_signup.html", title="Fleamarket | Signup",                            
                error_message="Invalid username",
                user_username_error="input_error", x=x, lan=lan, languages=languages)
        
        if "lastname" in str(ex):
            return render_template("view_signup.html", title="Fleamarket | Signup",
                error_message="Invalid last name",
                user_last_name_error="input_error", x=x, lan=lan, languages=languages)
        
        if "user_email" in str(ex):
            return render_template("view_signup.html", 
                error_message="Invalid email address or email already exists",
                user_email_error="input_error", 
                x=x, lan=lan, languages=languages)
        
        if "password" in str(ex):
            return render_template("view_signup.html", title="Fleamarket | Signup",
                error_message="Invalid password",
                user_password_error="input_error", x=x, lan=lan, languages=languages)
            
        return render_template("view_signup.html", title="Fleamarket | Signup",
            error_message=str(ex), x=x, lan=lan, languages=languages)

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/verify/<verification_key>")
def verify_email(verification_key):
    try:
        db, cursor = x.db()

        # Check if verification key exists
        q = "SELECT * FROM users WHERE user_verification_key = %s"
        cursor.execute(q, (verification_key,))
        user = cursor.fetchone()

        if not user:
            raise Exception("Invalid verification link")

        # Get current epoch time
        current_time = int(time.time())

        # Mark the user as verified with current timestamp
        q = "UPDATE users SET user_verified_at = %s, user_verification_key = NULL WHERE user_pk = %s"
        cursor.execute(q, (current_time, user["user_pk"]))

        if cursor.rowcount != 1:
            raise Exception("Error verifying account")

        db.commit()

        # Return a redirect to the login page with success message
        return redirect(url_for("view_login", message="Your account has been successfully verified. You can now log in."))

    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        return redirect(url_for("view_login", error_message="Error verifying account: " + str(ex)))

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/login")
def view_login():
    try:
        lan = session.get("language", "en")
        active_login = "active"
        error_message = request.args.get("error_message", "")
        message = request.args.get("message", "")
        return render_template("view_login.html", title="Fleamarket | Login", x=x, active_login=active_login, message=message, error_message=error_message, lan=lan, languages=languages)
    except Exception as ex:
        ic(ex)
    finally:
        pass


##############################
@app.post("/login")
def login():
    try:
        lan = session.get("language", "en")
        user_username = x.validate_user_username()
        user_password = x.validate_user_password()
        
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_username = %s AND user_deleted_at = 0 AND user_blocked_at = 0"
        cursor.execute(q, (user_username,))
        user = cursor.fetchone()
        
        if not user: raise Exception("Invalid credentials")

        if user["user_blocked_at"] != 0:
            raise Exception("Your account has been blocked by an administrator")
        
        if not check_password_hash(user["user_password"], user_password):
            raise Exception("Invalid credentials")
            
        if user["user_verified_at"] == 0:
            raise Exception("Please verify your email before logging in. Check your inbox for a verification link.")
            
        user.pop("user_password", None)
        session["user"] = user
        
        # Return MixHTML that updates both the page and the navigation
        new_nav = render_template("_nav.html")
        
        return f"""
        <mixhtml mix-redirect="/profile">
            <mixhtml mix-replace="nav">
                {new_nav}
            </mixhtml>
        </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return f"""
        <mixhtml mix-top="#login">
            <div class="error-message">Error updating profile: {str(ex)}</div>
        </mixhtml>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/logout")
def logout():
    try:
        session.clear() 
        new_nav = render_template("_nav.html")  # Render updated nav without user
        return f"""
        <mixhtml mix-redirect="/">
            <mixhtml mix-replace="nav">
                {new_nav}
            </mixhtml>
        </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return redirect(url_for("view_index"))
    finally:
        pass


##############################
@app.get("/profile")
def view_profile():
    try:
        is_session = False
        if "user" in session and session["user"]:
            is_session = True
            active_profile = "active"
            lan = session.get("language", "en")
            return render_template("view_profile.html", title="Fleamarket | Profile", user=session["user"], 
                                x=x, active_profile=active_profile, is_session=is_session, 
                                lan=lan, languages=languages)
        else:
            return redirect(url_for("view_login"))
    except Exception as ex:
        ic(ex)
        return redirect(url_for("view_login"))
    finally:
        pass


##############################
@app.get("/your-fleamarket")
def view_user_fleamarket():
    try:
        if "user" not in session or not session["user"]:
            return redirect(url_for("view_login", error_message="Please login"))
        
        lan = session.get("language", "en")
        user_pk = session["user"]["user_pk"]
        message = request.args.get("message", "")
        error_message = request.args.get("error_message", "")
        
        db, cursor = x.db()
        # Get main fleamarket data
        q = "SELECT * FROM items WHERE item_user_fk = %s AND Item_deleted_at = 0 LIMIT 1"
        cursor.execute(q, (user_pk,))
        user_fleamarket = cursor.fetchone()
        
        # Get additional images if fleamarket exists
        additional_images = []
        if user_fleamarket:
            q_images = "SELECT image_name FROM images WHERE image_item_fk = %s"
            cursor.execute(q_images, (user_fleamarket["item_pk"],))
            additional_images = [row['image_name'] for row in cursor.fetchall()]
        
        return render_template("view_user_fleamarket.html", 
                            title="Fleamarket | Your fleamarket", 
                            user_fleamarket=user_fleamarket,
                            additional_images=additional_images,
                            message=message,
                            error_message=error_message,
                            lan=lan, languages=languages,
                            x=x)
    except Exception as ex:
        ic(ex)
        return redirect(url_for("view_index", error_message="Error loading your fleamarket"))
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/your-fleamarket")
def add_fleamarket():
    try:
        if "user" not in session or not session["user"]:
            return redirect(url_for("view_login", error_message="Please login"))
        
        user_pk = session["user"]["user_pk"]
        item_pk = uuid.uuid4().hex
        item_name = x.validate_item_name()
        item_address = x.validate_item_address()
        item_price = x.validate_item_price()
        item_latitude = x.validate_item_latitude()  
        item_longitude = x.validate_item_longitude()
        item_created_at = int(time.time())
        
        # Handle image uploads
        images = x.validate_item_images()
        if not images:
            raise Exception("Please upload at least one image")
            
        # Use the first image as the main image
        item_image = images[0]

        db_conn, cursor = x.db()
        
        # Check if user already has a fleamarket
        q = "SELECT * FROM items WHERE item_user_fk = %s AND Item_deleted_at = 0"
        cursor.execute(q, (user_pk,))
        if cursor.fetchone():
            raise Exception("You already have a fleamarket. Please edit or delete it first.")

        # Insert the main fleamarket record
        q = """INSERT INTO items 
        (item_pk, item_user_fk, item_name, item_address, item_image, item_price, item_lat, 
        item_lon, item_created_at, item_updated_at, Item_deleted_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.execute(q, (item_pk, user_pk, item_name, item_address, item_image, 
                        item_price, item_latitude, item_longitude, 
                        item_created_at, 0, 0))

        # If there are additional images, store them in the images table
        if len(images) > 1:
            for img in images[1:]:
                img_pk = uuid.uuid4().hex
                q_img = """INSERT INTO images 
                        (image_pk, image_item_fk, image_name, image_created_at) 
                        VALUES (%s, %s, %s, %s)"""
                cursor.execute(q_img, (img_pk, item_pk, img, item_created_at))

        db_conn.commit()
        
        return f"""
        <mixhtml mix-redirect="/your-fleamarket?message=Fleamarket added successfully">
        </mixhtml>
        """
        
    except Exception as ex:
        ic(ex)
        if "db_conn" in locals(): db_conn.rollback()
        
        return f"""
        <mixhtml mix-replace=".message-container">
            <div class="message-container">
                <div class="error-message">Error: {str(ex)}</div>
            </div>
        </mixhtml>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db_conn" in locals(): db_conn.close()


##############################
@app.post("/your-fleamarket/update")
def update_fleamarket():
    try:
        if "user" not in session or not session["user"]:
            return redirect(url_for("view_login", error_message="Please login"))
        
        user_pk = session["user"]["user_pk"]
        item_pk = request.form.get("item_pk", "").strip()
        item_name = x.validate_item_name()
        item_address = x.validate_item_address()
        item_price = x.validate_item_price()
        item_latitude = x.validate_item_latitude()  
        item_longitude = x.validate_item_longitude()
        item_updated_at = int(time.time())

        db_conn, cursor = x.db()
        
        # Verify that this item belongs to the current user
        q = "SELECT * FROM items WHERE item_pk = %s AND item_user_fk = %s AND item_deleted_at = 0"
        cursor.execute(q, (item_pk, user_pk))
        if not cursor.fetchone():
            raise Exception("Fleamarket not found or you don't have permission to edit it")
        
        # Handle image uploads if provided
        images = x.validate_item_images()
        if images:
            # Use first image as main image
            item_image = images[0]
            
            # Update main image in items table
            q = """UPDATE items SET 
                item_name = %s, 
                item_address = %s, 
                item_image = %s, 
                item_price = %s, 
                item_lat = %s, 
                item_lon = %s, 
                item_updated_at = %s 
                WHERE item_pk = %s AND item_user_fk = %s"""

            cursor.execute(q, (item_name, item_address, item_image, item_price, 
                            item_latitude, item_longitude, item_updated_at, 
                            item_pk, user_pk))
                
            # Delete old additional images
            q_del = "DELETE FROM images WHERE image_item_fk = %s"
            cursor.execute(q_del, (item_pk,))
            
            # Add any additional images
            if len(images) > 1:
                for img in images[1:]:
                    img_pk = uuid.uuid4().hex
                    q_img = """INSERT INTO images 
                            (image_pk, image_item_fk, image_name, image_created_at) 
                            VALUES (%s, %s, %s, %s)"""
                    cursor.execute(q_img, (img_pk, item_pk, img, item_updated_at))
        else:
            # Update without changing images
            q = """UPDATE items SET 
                item_name = %s, 
                item_address = %s, 
                item_price = %s, 
                item_lat = %s, 
                item_lon = %s, 
                item_updated_at = %s 
                WHERE item_pk = %s AND item_user_fk = %s"""

            cursor.execute(q, (item_name, item_address, item_price, 
                            item_latitude, item_longitude, item_updated_at, 
                            item_pk, user_pk))

        db_conn.commit()
        
        return f"""
        <mixhtml mix-replace=".message-container">
            <div class="message-container">
                <div class="success-message">Fleamarket updated successfully!</div>
            </div>
        </mixhtml>
        """
        
    except Exception as ex:
        ic(ex)
        if "db_conn" in locals(): db_conn.rollback()
        
        return f"""
        <mixhtml mix-replace=".message-container">
            <div class="message-container">
                <div class="error-message">Error: {str(ex)}</div>
            </div>
        </mixhtml>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db_conn" in locals(): db_conn.close()


@app.post("/your-fleamarket/delete")
def delete_fleamarket():
    try:
        if "user" not in session or not session["user"]:
            return redirect(url_for("view_login", error_message="Please login"))
        
        user_pk = session["user"]["user_pk"]
        item_pk = request.form.get("item_pk", "").strip()

        db_conn, cursor = x.db()
        
        # First delete associated images
        q_del_img = "DELETE FROM images WHERE image_item_fk = %s"
        cursor.execute(q_del_img, (item_pk,))
        
        # Then soft-delete the fleamarket
        q = """UPDATE items SET 
            item_deleted_at = %s 
            WHERE item_pk = %s AND item_user_fk = %s"""
        cursor.execute(q, (int(time.time()), item_pk, user_pk))
        
        db_conn.commit()
        
        return f"""
        <mixhtml mix-redirect="/your-fleamarket?message=Fleamarket deleted successfully">
        </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        if "db_conn" in locals(): db_conn.rollback()
        return f"""
        <mixhtml mix-replace=".message-container">
            <div class="message-container">
                <div class="error-message">Error: {str(ex)}</div>
            </div>
        </mixhtml>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db_conn" in locals(): db_conn.close()


##############################
@app.get("/update-profile")
def view_update_profile():
    try:
        if "user" not in session or not session["user"]:
            return redirect(url_for("view_login", error_message="Please login"))
        
        lan = session.get("language", "en")
        user = session["user"]
        user_pk = user["user_pk"]
        
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_pk = %s"
        cursor.execute(q, (user_pk,))
        user_data = cursor.fetchone()
        
        return render_template("view_update_profile.html", title="Fleamarket | Update Profile",
                            user=user_data, x=x, lan=lan, languages=languages)
    except Exception as ex:
        ic(ex)
        return redirect(url_for("view_login", error_message="System error"))
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/update-profile")
def update_profile():
    try:
        if "user" not in session or not session["user"]:
            return redirect(url_for("view_login", error_message="Please login"))
        
        user_pk = session["user"]["user_pk"]
        user_username = x.validate_user_username()
        user_email = x.validate_user_email()
        
        current_password = request.form.get("current_password", "").strip()
        if not current_password:
            raise Exception("Current password is required")
        
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_pk = %s"
        cursor.execute(q, (user_pk,))
        user = cursor.fetchone()
        
        if not user:
            raise Exception("User not found")
        
        if not check_password_hash(user["user_password"], current_password):
            raise Exception("Current password is incorrect")
        
        # Check if user wants to change password
        hashed_password = user["user_password"]  # Keep current by default
        
        if new_password:
            # Validate new password format
            if not re.match(x.USER_PASSWORD_REGEX, new_password):
                raise Exception(f"New password must be {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters")
            
            # Check if passwords match
            if new_password != confirm_password:
                raise Exception("New passwords do not match")
            
            # Hash the new password
            hashed_password = generate_password_hash(new_password)
        
        q = """UPDATE users
            SET user_username = %s, user_email = %s, user_password = %s, user_updated_at = %s
            WHERE user_pk = %s"""
        
        cursor.execute(q, (user_username, user_email, hashed_password, int(time.time()), user_pk))
        
        if cursor.rowcount != 1:
            raise Exception("System under maintenance")
            
        db.commit()
        
        # Update session data (-password)
        session["user"]["user_username"] = user_username
        session["user"]["user_email"] = user_email
        
        return f"""
        <mixhtml mix-top=".edit-profile">
            <div class="success-message">Profile updated successfully!</div>
        </mixhtml>
        """
        
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        
        return f"""
        <mixhtml mix-top=".edit-profile">
            <div class="error-message">Error updating profile: {str(ex)}</div>
        </mixhtml>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/reset-password")
def view_reset_password():
    try:
        lan = session.get("language", "en")
        message = request.args.get("message", "")
        error_message = request.args.get("error_message", "")
        return render_template("view_reset_password.html", title="Fleamarket | Reset Password",
                            message=message, error_message=error_message, x=x, 
                            lan=lan, languages=languages)
    except Exception as ex:
        ic(ex)
        return redirect(url_for("view_login", error_message="System error"))


##############################
@app.post("/reset-password")
def reset_password_request():
    try:
        user_email = x.validate_user_email()
        
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s AND user_deleted_at = 0"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        
        if not user:
            return render_template("view_reset_password.html", 
                message="If your email is registered, you will receive a password reset link shortly.",
                x=x)
        
        reset_key = uuid.uuid4().hex
        
        # Store the reset token and set expiration (1 hour)
        expiration_time = int(time.time()) + 3600
        
        # Update user with reset token
        q = "UPDATE users SET user_verification_key = %s, user_updated_at = %s WHERE user_pk = %s"
        cursor.execute(q, (reset_key, int(time.time()), user["user_pk"]))
        
        if cursor.rowcount != 1: 
            raise Exception("System under maintenance")
        
        db.commit()
        
        # Send password reset email
        x.send_password_reset_email(user["user_name"], user["user_last_name"], reset_key, user_email)
        
        return render_template("view_reset_password.html", 
            message="If your email is registered, you will receive a password reset link shortly.",
            x=x)
        
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        return render_template("view_reset_password.html", 
            error_message="An error occurred. Please try again.",
            x=x)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/reset-password/<reset_key>")
def view_new_password(reset_key):
    try:
        lan = session.get("language", "en")
        # Verify the reset key exists and is not expired
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_verification_key = %s AND user_deleted_at = 0"
        cursor.execute(q, (reset_key,))
        user = cursor.fetchone()
        
        if not user:
            return redirect(url_for("view_login", error_message="Invalid or expired reset link"))
        
        # Check if the reset link is expired (older than 1 hour)
        current_time = int(time.time())
        if current_time - user["user_updated_at"] > 3600:
            return redirect(url_for("view_login", error_message="Reset link expired. Please request a new one."))
            
        return render_template("view_new_password.html", reset_key=reset_key, x=x, 
                            lan=lan, languages=languages)
        
    except Exception as ex:
        ic(ex)
        return redirect(url_for("view_login", error_message="System error"))
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/reset-password/<reset_key>")
def update_password(reset_key):
    try:
        # Verify the reset key exists
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_verification_key = %s AND user_deleted_at = 0"
        cursor.execute(q, (reset_key,))
        user = cursor.fetchone()
        
        if not user:
            return redirect(url_for("view_login", error_message="Invalid or expired reset link"))
        
        # Check if the reset link is expired (older than 1 hour)
        current_time = int(time.time())
        if current_time - user["user_updated_at"] > 3600:
            return redirect(url_for("view_login", error_message="Reset link expired. Please request a new one."))
        
        # Validate password
        user_password = x.validate_user_password()
        user_password_confirm = request.form.get("user_password_confirm", "").strip()
        
        if user_password != user_password_confirm:
            return render_template("view_new_password.html", 
                error_message="Passwords do not match", 
                reset_key=reset_key, x=x)
        
        # Hash new password and update user
        hashed_password = generate_password_hash(user_password)
        
        q = "UPDATE users SET user_password = %s, user_verification_key = NULL, user_updated_at = %s WHERE user_pk = %s"
        cursor.execute(q, (hashed_password, current_time, user["user_pk"]))
        
        if cursor.rowcount != 1:
            raise Exception("Could not update password")
            
        db.commit()
        
        return redirect(url_for("view_login", message="Password has been reset successfully. You can now log in."))
        
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        return render_template("view_new_password.html", 
            error_message=str(ex), reset_key=reset_key, x=x)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/delete-account")
def delete_account():
    try:
        if "user" not in session or not session["user"]:
            return redirect(url_for("view_login", error_message="Please login"))
        
        user_pk = session["user"]["user_pk"]
        
        # Get password for verification
        confirm_password = request.form.get("confirm_password", "").strip()
        if not confirm_password:
            return f"""
            <mixhtml mix-replace=".delete-message-area">
                <div class="error-message">Please enter your password to confirm deletion</div>
            </mixhtml>
            """
        
        # Verify user exists and password is correct
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_pk = %s"
        cursor.execute(q, (user_pk,))
        user = cursor.fetchone()
        
        if not user:
            raise Exception("User not found")
        
        # Verify the password
        if not check_password_hash(user["user_password"], confirm_password):
            return f"""
            <mixhtml mix-replace=".delete-message-area">
                <div class="error-message">Incorrect password</div>
            </mixhtml>
            """
        
        # Store user email for notification
        user_email = user["user_email"]
        user_name = user["user_name"]
        user_lastname = user["user_last_name"]
        
        # Soft delete the user by setting deleted_at timestamp
        current_time = int(time.time())
        q = "UPDATE users SET user_deleted_at = %s WHERE user_pk = %s"
        cursor.execute(q, (current_time, user_pk))
        
        if cursor.rowcount != 1:
            raise Exception("Could not delete account")
            
        db.commit()
        
        # Send notification email
        x.send_account_deletion_email(user_name, user_lastname, user_email)
        
        # Clear session
        session.clear()
        
        # Return success and redirect
        return f"""
        <mixhtml mix-redirect="/login">
            <mixhtml mix-replace="nav">
                {render_template("_nav.html")}
            </mixhtml>
        </mixhtml>
        """
        
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        
        return f"""
        <mixhtml mix-replace=".delete-message-area">
            <div class="error-message">Error: {str(ex)}</div>
        </mixhtml>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/search")
def search():
    try:
        search_for = request.args.get("q", "") 
        # TODO: validate search_for
        db, cursor = x.db()
        q = "SELECT * FROM items WHERE item_name LIKE %s"
        cursor.execute(q, (f"{search_for}%",))
        rows = cursor.fetchall()
        ic(rows)
        return rows
    except Exception as ex:
        ic(ex)
        return "x", 400


##############################
@app.patch("/block/<user_pk>")
def block_user(user_pk):
    try:
        # Check if user is admin
        if ("user" not in session or not session["user"] or 
            not session["user"].get("user_is_admin", 0) == 1):
            return "Admin access required", 403

        db, cursor = x.db()

        q_user = "SELECT user_name, user_last_name, user_email FROM users WHERE user_pk = %s"
        cursor.execute(q_user, (user_pk,))
        user_data = cursor.fetchone()
        
        if not user_data:
            raise Exception("User not found")
            
        # Block the user
        q = "UPDATE users SET user_blocked_at = %s WHERE user_pk = %s"
        blocked_at = int(time.time())
        cursor.execute(q, (blocked_at, user_pk))
        db.commit()
        
        # Send email notification
        x.send_user_blocked_email(
            user_data["user_name"],
            user_data["user_last_name"],
            user_data["user_email"]
        )
        
        user = {
            "user_pk": user_pk
        }
        button_unblock = render_template("_button_unblock_user.html", user=user)
        return f"""
        <mixhtml mix-replace="#block-{user_pk}">
            {button_unblock}
        </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.patch("/unblock/<user_pk>")
def unblock_user(user_pk):
    try:
        # Connect to the db and unblock the user
        db, cursor = x.db()
        q = "UPDATE users SET user_blocked_at = %s WHERE user_pk = %s"  
        cursor.execute(q, (0, user_pk))
        db.commit()              
        user = {
            "user_pk":user_pk
        }          
        button_block = render_template("_button_block_user.html", user=user)
        return f"""
        <mixhtml mix-replace="#unblock-{user_pk}">
            {button_block}
        </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.patch("/block-item/<item_pk>")
def block_item(item_pk):
    try:
        if ("user" not in session or not session["user"] or 
            not session["user"].get("user_is_admin", 0) == 1):
            return "Admin access required", 403
            
        db, cursor = x.db()
        
        q_item = "SELECT item_name, item_user_fk FROM items WHERE item_pk = %s"
        cursor.execute(q_item, (item_pk,))
        item_data = cursor.fetchone()
        
        if not item_data or not item_data["item_user_fk"]:
            # Item not found or no user associated with it
            pass
        else:
            # Get the owner's details for email notification
            q_user = "SELECT user_name, user_last_name, user_email FROM users WHERE user_pk = %s"
            cursor.execute(q_user, (item_data["item_user_fk"],))
            user_data = cursor.fetchone()
            
            if user_data:
                # Send email notification to the item's owner
                x.send_item_blocked_email(
                    user_data["user_name"],
                    user_data["user_last_name"],
                    item_data["item_name"],
                    user_data["user_email"]
                )
        
        q = "UPDATE items SET item_blocked_at = %s WHERE item_pk = %s"
        blocked_at = int(time.time())
        cursor.execute(q, (blocked_at, item_pk))
        db.commit()
        
        item = {
            "item_pk": item_pk
        }
        button_unblock = render_template("_button_unblock_item.html", item=item)
        return f"""
        <mixhtml mix-replace="#block-item-{item_pk}">
            {button_unblock}
        </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.patch("/unblock-item/<item_pk>")
def unblock_item(item_pk):
    try:
        # Check if user is admin
        if ("user" not in session or not session["user"] or 
            not session["user"].get("user_is_admin", 0) == 1):
            return "Admin access required", 403
            
        db, cursor = x.db()
        # Use the proper item_blocked_at field
        q = "UPDATE items SET item_blocked_at = %s WHERE item_pk = %s"  
        cursor.execute(q, (0, item_pk))
        db.commit()              
        item = {
            "item_pk": item_pk
        }          
        button_block = render_template("_button_block_item.html", item=item)
        return f"""
        <mixhtml mix-replace="#unblock-item-{item_pk}">
            {button_block}
        </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/admin")
def view_admin():
    try:
        lan = session.get("language", "en")
        if ("user" not in session or not session["user"] or 
            not session["user"].get("user_is_admin", 0) == 1):
            return redirect(url_for("view_login", error_message="Admin access required"))
            
        db, cursor = x.db()
        
        # Get users
        q_users = "SELECT * FROM users"
        cursor.execute(q_users)
        users = cursor.fetchall()
        
        # Get items (fleamarkets)
        q_items = "SELECT * FROM items"
        cursor.execute(q_items)
        items = cursor.fetchall()
        
        return render_template("view_admin.html", title="Fleamarket | Admin Dashboard", 
                    users=users, items=items, lan=lan, languages=languages)
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()
