from flask import Flask, render_template, session, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
import x
import time
import uuid
import os
import redis
import json

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


##############################
@app.get("/")
def view_index():
    try:
        db, cursor = x.db()
        q = "SELECT * FROM items ORDER BY item_created_at LIMIT 2"
        cursor.execute(q)
        items = cursor.fetchall()
        return render_template("view_index.html", title="Fleamarket | Home", items=items)
    except Exception as ex:
        ic(ex)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/items/<item_pk>")
def get_item_by_pk(item_pk):
    try:
        db, cursor = x.db()
        q = "SELECT * FROM items WHERE item_pk = %s"
        cursor.execute(q, (item_pk,))
        item = cursor.fetchone()
        html_item = render_template("_item.html", item=item)
        return f"""
            <mixhtml mix-replace="#item">
                {html_item}
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
        # worst case, we cannot control exceptions
        return """
            <mixhtml mix-top="body">
                ups
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
        q = "SELECT * FROM items ORDER BY item_created_at LIMIT %s OFFSET %s"
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
        # worst case, we cannot control exceptions
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
        return render_template("view_signup.html", title="Fleamarket | Signup", x=x)
    except Exception as ex:
        ic(ex)
    finally:
        pass


##############################
@app.post("/signup")
def signup():
    try:
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        user_username = x.validate_user_username()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        hashed_password = generate_password_hash(user_password)
        user_created_at = int(time.time())
        user_pk = uuid.uuid4().hex  # Generate UUID for primary key

        q = """INSERT INTO users 
        (user_pk, user_username, user_name, user_last_name, user_email, 
        user_password, user_created_at, user_updated_at, user_deleted_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        db, cursor = x.db()
        cursor.execute(q, (user_pk, user_username, user_name, user_last_name, 
                        user_email, hashed_password, user_created_at, 0, 0))

        if cursor.rowcount != 1: raise Exception("System under maintenance")
        db.commit()

        return redirect(url_for("view_login", message="Signup successful"))
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        old_values = request.form.to_dict()
        
        if "username" in str(ex):
            old_values.pop("user_username", None)
            return render_template("view_signup.html", title="Fleamarket | Signup",                            
                error_message="Invalid username", old_values=old_values,
                user_username_error="input_error", x=x)
        if "lastname" in str(ex):
            old_values.pop("user_last_name", None)
            return render_template("view_signup.html", title="Fleamarket | Signup",
                error_message="Invalid last name", old_values=old_values,
                user_last_name_error="input_error", x=x)
        if "email" in str(ex):
            old_values.pop("user_email", None)
            return render_template("view_signup.html", title="Fleamarket | Signup",
                error_message="Invalid email", old_values=old_values,
                user_email_error="input_error", x=x)
        if "password" in str(ex):
            old_values.pop("user_password", None)
            return render_template("view_signup.html", title="Fleamarket | Signup",
                error_message="Invalid password", old_values=old_values,
                user_password_error="input_error", x=x)
            
        return render_template("view_signup.html", title="Fleamarket | Signup",
            error_message=str(ex), old_values=old_values, x=x)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/login")
def view_login():
    try:
        active_login = "active"
        error_message = request.args.get("error_message", "")
        message = request.args.get("message", "")
        return render_template("view_login.html", title="Fleamarket | Login", x=x, active_login=active_login, message=message, error_message=error_message)
    except Exception as ex:
        ic(ex)
    finally:
        pass


##############################
@app.post("/login")
def login():
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s AND user_deleted_at = 0"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        
        if not user: raise Exception("Invalid credentials")
        
        if not check_password_hash(user["user_password"], user_password):
            raise Exception("Invalid credentials")
            
        # Remove password from session data
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
        return render_template("view_login.html", title="Fleamarket | Login", 
                            error_message=str(ex), x=x)
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
            return render_template("view_profile.html", title="Profile", user=session["user"], 
                                x=x, active_profile=active_profile, is_session=is_session)
        else:
            return redirect(url_for("view_login"))
    except Exception as ex:
        ic(ex)
        return redirect(url_for("view_login"))
    finally:
        pass




