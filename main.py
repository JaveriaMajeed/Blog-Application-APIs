# imporing libraries
from flask import Flask, render_template,request,redirect, url_for, session,flash, jsonify
import psycopg2 
import os
from constant import *
import re 
from functools import wraps
import jwt
from datetime import datetime, timedelta

# connecting with the database
conn = psycopg2.connect(host = hostname, dbname = database, password = pwd ,user = username, port = port_id)
cursor = conn.cursor()

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = os.urandom(24)

# for checking email format
def email_validation(email):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+'
    return re.match(email_pattern, email) is not None

# for token validation
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get("token")
        if not token:
            return jsonify({"message": "token is missing"})
        try: 
            payload = jwt.decdoe(token , app.config['SECRET_KEY'])
        except:
            return jsonify({"message": "token is invalid!"})
    return decorated


# login route
@app.route("/")
def login():
    return render_template('login.html')

# registeration route
@app.route("/register") 
def register():
    return render_template('register.html')

# homepage route
@token_required
@app.route("/home")
def home():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect("/")

# comment route
@app.route("/comment")
def comment():
        if 'user_id' in session:
            return render_template('comment.html')
        else:
            return redirect("/")
   
# for creating a post
@app.route("/post")
def post():
    if 'user_id' in session:
        return render_template('post.html')
    else:
        return redirect("/")


@app.route("/login_validation", methods = ['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('Password')
  
    cursor.execute(''' SELECT * FROM Users WHERE email LIKE '{}' AND password LIKE '{}' ''' 
              .format(email,password))
    user = cursor.fetchall()
    if len(user)>0:
        session['user_id'] = user[0][3]
        # session['Logged_in'] = True
        token = jwt.encode({
            'user':user[0][0],
            'exp': str(datetime.utcnow() + timedelta(seconds = 120))
        }, app.config['SECRET_KEY'] )
        
        return jsonify({"token": token})
    else:
        return redirect('/')
    
@app.route("/reg_validation", methods = ['POST'])
def reg_validation():
    name = request.form.get('name')
    password = request.form.get('password')
    email = request.form.get('email')
    if not email_validation(email):
        flash('Invalid email address format', 'error')

    # checking for duplicate username
    cursor.execute(''' SELECT name FROM users WHERE name = '{}' ''' .format(name))
    existing_username = cursor.fetchall()
    if len(existing_username)>0:
        return jsonify ({ 'message':'Username is already in use. Please choose a different one.'})
    
    # checking for duplicate email
    cursor.execute(''' SELECT email FROM Users WHERE email = '{}' ''' .format(email))
    existing_email = cursor.fetchall()
    if len(existing_email)>0:
        return jsonify ({ 'message': 'Email address is already registered. Please use a different email.'})

    else:
        cursor.execute(''' INSERT INTO Users (name, email, password) VALUES ('{}', '{}', '{}')'''.format(name,email,password))
        conn.commit()
        return redirect ('/')
    

@app.route("/post_creation", methods = ['POST'])
def post_creation():
    author_name = request.form.get('name')
    title = request.form.get('title')
    content = request.form.get('content')

    cursor.execute(''' INSERT INTO Post (author, title, content,date) VALUES ('{}', '{}', '{}',CURRENT_TIMESTAMP) ''' .format(author_name, title, content))
    conn.commit()
    return redirect(url_for('display_posts'))
              
@app.route('/display_posts')
def display_posts():
    cursor.execute('''SELECT title, content, date, author FROM Post ORDER BY date DESC LIMIT 2''')
    post = cursor.fetchall()
    return render_template('index.html', posts=post)

@app.route("/post_comment", methods = ['POST'])
def post_comment():
    name = request.form.get("name")
    comment = request.form.get("comment")

    cursor.execute(''' INSERT INTO Post_comment (name, comments) VALUES ('{}', '{}') ''' .format(name, comment))
    conn.commit()
    flash("Posted comment Successfully")

    return redirect(url_for('display_comment'))

@app.route('/display_comment')
def display_comment():
    cursor.execute(''' SELECT comments, name FROM Post_comment ORDER BY comment_id DESC LIMIT 3 ''')
    comment = cursor.fetchall()
    return render_template('comment.html', comment=comment)

if __name__ == "__main__":
    app.run(debug = True)
