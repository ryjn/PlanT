from flask import Flask, render_template, json, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask import request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rjk.03260211'
app.config['MYSQL_DB'] = 'PlanT'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, user_id, first_name, last_name, email, phone, username, password):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    user = "SELECT * FROM Users WHERE user_id=%s" % (user_id)
    cur = mysql.connection.cursor()
    cur.execute(user)
    user = cur.fetchall()

    if user:
        cur_user = User(user[0]['user_id'], user[0]['first_name'], user[0]['last_name'], user[0]['email'], user[0]['phone'], user[0]['username'], user[0]['password'])
        return cur_user
    
    return

# Routes

# Home
@app.route('/')
def root():
    return render_template("index.j2")

# Need to update with actual login credentials
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated is True:
        return redirect('/dashboard')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Create User object
        user = "SELECT * FROM Users WHERE username = '%s'" % (username)
        cur = mysql.connection.cursor()
        cur.execute(user)
        user = cur.fetchall()
        
        if user:
            user_id = user[0]['user_id']
            first_name = user[0]['first_name']
            last_name = user[0]['last_name']
            email = user[0]['email']
            phone = user[0]['phone']
            user_username = user[0]['username']
            user_password = user[0]['password']
            cur_user = User(user_id, first_name, last_name, email, phone, user_username, user_password)

            # Verify password
            if check_password_hash(cur_user.password, password):
                flash('Logged in successfully! Welcome back.', category='success')
                login_user(cur_user)
                return redirect("/dashboard")
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist. Please try again.', category='error')

    return render_template('login.j2')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out succesfully. Come back soon!', category='success')
    return redirect('/login')

# Sign Up
@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        if request.form.get("register"):
            # Get registration inputs
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            username = request.form['username']
            password1 = request.form['password1']
            password2 = request.form['password2']

            # Check if email exists
            email_exist = "SELECT EXISTS (SELECT * FROM Users WHERE email='%s') AS email_valid" % (email)
            cur = mysql.connection.cursor()
            cur.execute(email_exist)
            email_valid = cur.fetchall()[0]['email_valid']

            # Check if username exists
            username_exist = "SELECT EXISTS (SELECT * FROM Users WHERE username='%s') AS username_valid" % (username)
            cur = mysql.connection.cursor()
            cur.execute(username_exist)
            username_valid = cur.fetchall()[0]['username_valid']

            # Validation
            if password1 != password2:
               flash('Passwords do not match.', category='error')
               return render_template('sign_up.j2')
            elif len(password1) < 7:
                flash('Password length is less than 7 characters.', category='error')
                return render_template('sign_up.j2')
            elif email_valid == 1:
                flash('Email already exists.', category='error')
                return render_template('sign_up.j2')
            elif len(username) < 4:
                flash('Username is less than 5 characters.', category='error')
                return render_template('sign_up.j2')
            elif username_valid == 1:
                flash('Username already exists.', category='error')
                return render_template('sign_up.j2')
            else:
                # Perform insert operations
                password = generate_password_hash(password1, method='scrypt')
                insert = "INSERT INTO Users (first_name, last_name, email, phone, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
                user_id = "SELECT LAST_INSERT_ID()"
                cur = mysql.connection.cursor()
                cur.execute(insert, (first_name, last_name,
                            email, phone, username, password))
                mysql.connection.commit()
                cur.execute(user_id)
                user_id = cur.fetchall()[0]['LAST_INSERT_ID()']

                # Create User object
                cur_user = User(user_id, first_name, last_name, email, phone, username, password)

                # Login new user
                login_user(cur_user)

                return redirect("/displayid")

    else:
        return render_template("sign_up.j2")

# Set display ID
@app.route('/displayid', methods=['POST', 'GET'])
def set_displayID():
    if request.method == 'POST':
        if request.form.get('displayID'):
            # Get display id
            display_id = request.form['displayID']

            # Query to add display id
            add_id = "UPDATE Users SET display_id = %s WHERE user_id = %s"
            
            # Execute query
            cur = mysql.connection.cursor()
            cur.execute(add_id, (display_id, current_user.id))
            mysql.connection.commit()

            # Redirect to dashboard
            flash('Sign-up successful! Welcome to PlanT.', category='success')
            return redirect('/dashboard')
        
    return render_template('display_id.j2')

# User dashboard
@app.route('/dashboard', methods=['POST', 'GET'])
def show_dashboard():
    if request.method == 'POST':
        if request.form.get('submit_event'):
            # Get Event info
            event_name = request.form['event_name']
            event_desc = request.form['event_desc']
            date = request.form['date']
            time = request.form['time']
            user_id = current_user.id
            
            # Check if event name exists
            get_event = "SELECT 1 FROM Events WHERE user_id=%s AND event_name=%s"

            # query to insert event
            add_event = "INSERT INTO Events (event_name, event_desc, date, time, user_id) VALUES (%s, %s, %s, %s, %s)"

            cur = mysql.connection.cursor()

            # Execute get_calendars
            cur.execute(get_event, (user_id, event_name))
            name_exists = cur.fetchall()

            # Check if calendar name already exists
            if name_exists:
                flash('Event name exists! Please use another name.', category='error')
                return redirect('/dashboard')
            else:
                # Execute add_calendar
                cur.execute(add_event, (event_name, event_desc, date, time, user_id))
                mysql.connection.commit()

                flash('Event created!', category='success')
                return redirect('/dashboard')
        if request.form.get('submit_user_add'):
            # Get Event info
            display_id = request.form['friend_displayID']
            user_id = current_user.id
            
            # Check if display_id exists
            displayID_exists = "SELECT EXISTS (SELECT * FROM Users WHERE display_id='%s') AS displayID_valid" % (display_id)

            # Check if already friends
            check_friend = "SELECT friend2_id FROM Friends WHERE friend1_id=%s AND friend2_id=%s"
            
            # Get Friend's ID
            friend_id = "SELECT user_id FROM Users WHERE display_id='%s'" % (display_id)

            # query to insert calendar
            add_user = "INSERT INTO Friends (friend1_id, friend2_id) VALUES (%s, %s)"

            cur = mysql.connection.cursor()

            # Execute get_calendars
            cur.execute(displayID_exists)
            displayID_exists = cur.fetchall()[0]['displayID_valid']

            # Check if calendar name already exists
            if displayID_exists != 1:
                flash('Display ID does not exist! Please try again.', category='error')
                return redirect('/dashboard')
            else:
                # Execute check_friend
                cur.execute(check_friend, (user_id, displayID_exists))
                friend_exists = cur.fetchall()

                if friend_exists:
                    flash('User already a friend!', category='error')
                    return redirect('/dashboard')
                else:
                    # Execute add_friend
                    cur.execute(friend_id)
                    friend_id = cur.fetchall()[0]['user_id']

                    cur.execute(add_user, (user_id, friend_id))
                    mysql.connection.commit()

                    flash('User added!', category='success')
                    return redirect('/dashboard')
    else:
        user_id = current_user.id
        
        # Query data
        event_data = "SELECT Events.event_name as Name, Events.event_desc as Description, Events.date as Date, Events.time as Time FROM Events WHERE Events.user_id=%s" % (user_id)
        event_check = "SELECT event_id FROM Events WHERE user_id=%s" % (user_id)

        friend_data = "SELECT Users.display_id as 'Display ID', Users.first_name as 'First Name', Users.last_name as 'Last Name' FROM Users WHERE Users.user_id=(SELECT friend2_id FROM Friends WHERE friend1_id=%s)" % (user_id)
        friend_check = "SELECT friend2_id FROM Friends WHERE friend1_id=%s" % (user_id)
        cur = mysql.connection.cursor()
        
        # Execute event_data query
        cur.execute(event_data)
        event_data = cur.fetchall()

        # Execute event_check
        cur.execute(event_check)
        event_check = cur.fetchall()

        # Execute friend_data query
        cur.execute(friend_data)
        friend_data = cur.fetchall()

        # Execute friend_check
        cur.execute(friend_check)
        friend_check = cur.fetchall()
        
        return render_template('dashboard.j2', event_data=event_data, event_check=event_check, friend_data=friend_data, friend_check=friend_check)
    
# Events
@app.route('/events', methods=['POST', 'GET'])
def show_event():
    if request.method == 'POST':
        if request.form.get('submit_event'):
            # Get Event info
            event_name = request.form['event_name']
            event_desc = request.form['event_desc']
            date = request.form['date']
            time = request.form['time']
            user_id = current_user.id
            
            # Check if event name exists
            get_event = "SELECT 1 FROM Events WHERE user_id=%s AND event_name=%s"

            # query to insert event
            add_event = "INSERT INTO Events (event_name, event_desc, date, time, user_id) VALUES (%s, %s, %s, %s, %s)"

            cur = mysql.connection.cursor()

            # Execute get_calendars
            cur.execute(get_event, (user_id, event_name))
            name_exists = cur.fetchall()

            # Check if calendar name already exists
            if name_exists:
                flash('Event name exists! Please use another name.', category='error')
                return redirect('/events')
            else:
                # Execute add_calendar
                cur.execute(add_event, (event_name, event_desc, date, time, user_id))
                mysql.connection.commit()

                flash('Event created!', category='success')
                return redirect('/events')
    else:
        user_id = current_user.id
        
        # Query data
        event_data = "SELECT Events.event_name as Name, Events.event_desc as Description, Events.date as Date, Events.time as Time FROM Events WHERE Events.user_id=%s" % (user_id)
        event_check = "SELECT event_id FROM Events WHERE user_id=%s" % (user_id)

        cur = mysql.connection.cursor()
        
        # Execute event_data query
        cur.execute(event_data)
        event_data = cur.fetchall()

        # Execute event_check
        cur.execute(event_check)
        event_check = cur.fetchall()
        
        return render_template('events.j2', event_data=event_data, event_check=event_check)

# User dashboard
@app.route('/friends', methods=['POST', 'GET'])
def show_friends():
    if request.method == 'POST':
        if request.form.get('submit_user_add'):
            # Get Event info
            display_id = request.form['friend_displayID']
            user_id = current_user.id
            
            # Check if display_id exists
            displayID_exists = "SELECT EXISTS (SELECT * FROM Users WHERE display_id='%s') AS displayID_valid" % (display_id)

            # Check if already friends
            check_friend = "SELECT friend2_id FROM Friends WHERE friend1_id=%s AND friend2_id=%s"
            
            # Get Friend's ID
            friend_id = "SELECT user_id FROM Users WHERE display_id='%s'" % (display_id)

            # query to insert calendar
            add_user = "INSERT INTO Friends (friend1_id, friend2_id) VALUES (%s, %s)"

            cur = mysql.connection.cursor()

            # Execute get_calendars
            cur.execute(displayID_exists)
            displayID_exists = cur.fetchall()[0]['displayID_valid']

            # Check if calendar name already exists
            if displayID_exists != 1:
                flash('Display ID does not exist! Please try again.', category='error')
                return redirect('/friends')
            else:
                # Execute check_friend
                cur.execute(check_friend, (user_id, displayID_exists))
                friend_exists = cur.fetchall()

                if friend_exists:
                    flash('User already a friend!', category='error')
                    return redirect('/friends')
                else:
                    # Execute add_friend
                    cur.execute(friend_id)
                    friend_id = cur.fetchall()[0]['user_id']

                    cur.execute(add_user, (user_id, friend_id))
                    mysql.connection.commit()

                    flash('User added!', category='success')
                    return redirect('/dashboard')
    else:
        user_id = current_user.id
        
        # Query data
        friend_data = "SELECT Users.display_id as 'Display ID', Users.first_name as 'First Name', Users.last_name as 'Last Name' FROM Users WHERE Users.user_id=(SELECT friend2_id FROM Friends WHERE friend1_id=%s)" % (user_id)
        friend_check = "SELECT friend2_id FROM Friends WHERE friend1_id=%s" % (user_id)
        cur = mysql.connection.cursor()

        # Execute friend_data query
        cur.execute(friend_data)
        friend_data = cur.fetchall()

        # Execute friend_check
        cur.execute(friend_check)
        friend_check = cur.fetchall()
        
        return render_template('friends.j2', friend_data=friend_data, friend_check=friend_check)
# Listener
if __name__ == "__main__":
    app.run(port=9452, debug=True)