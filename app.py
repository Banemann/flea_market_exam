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
        html_item = render_template("_item.html", item=item, standalone=True)
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
        return render_template("page_signup.html", title="Fleamarket | Signup", x=x)
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

        q = """INSERT INTO users 
        (user_pk, user_name, user_last_name, user_username, user_email, 
        user_password, user_created_at, user_updated_at, user_deleted_at) 
        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)"""

        db, cursor = x.db()
        # Modified parameters without verification fields
        cursor.execute(q, (user_name, user_last_name, user_username, user_email,
                        hashed_password, user_created_at, 0, 0))

        if cursor.rowcount != 1: raise Exception("System under maintenance")
        db.commit()

        return redirect(url_for("view_login", message="Signup successful"))
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        # request.form is a tuple
        old_values = request.form.to_dict()
        if "username" in str(ex):
            old_values.pop("user_username", None)
            return render_template("page_signup.html",                                   
                error_message="Invalid username", old_values=old_values,
                user_username_error="input_error", x=x)
        if "firstname" in str(ex):
            old_values.pop("user_name", None)
        return render_template("view_signup.html",
        error_message="Invalid name", old_values=old_values,
        user_name_error="input_error", x=x)

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
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        ic(user)
        if not user: raise Exception("User not found")
        if not check_password_hash(user["user_password"], user_password):
            raise Exception("Invalid credentials")
        user.pop("user_password")
        session["user"] = user
        
        # Remove this verification check
        # if user["user_verified_at"] == 0:
        #    raise Exception("Please verify your email")

        return redirect(url_for("view_profile"))
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        
        # Add return statement for exceptions
        active_login = "active"
        if "email" in str(ex).lower():
            return render_template("view_login.html", title="Login", active_login=active_login,
                                error_message=str(ex), user_email_error="input_error", x=x)
        elif "password" in str(ex).lower() or "credentials" in str(ex).lower():
            return render_template("view_login.html", title="Login", active_login=active_login,
                                error_message=str(ex), user_password_error="input_error", x=x)
        else:
            return render_template("view_login.html", title="Login", active_login=active_login,
                                error_message=str(ex), x=x)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/logout")
def logout():
    try:
        session.pop("user")
        return redirect(url_for("view_login"))
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




