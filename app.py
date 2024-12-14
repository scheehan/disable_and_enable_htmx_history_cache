import sys
sys.dont_write_bytecode = True

from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash
from utils import login_required, set_session

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
                                'connect_args': {"timeout": 10}
                                           }
app.config['SECRET_KEY'] = '59a0dda31bcb0e9819dd63b87deebd97bf1b42cb535e1952048afdedd7a9b58e'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route('/')
@login_required
def index():
    
    myusername = session['username']

    return render_template('index.html', username=myusername)

@app.route('/articles/<int:param>/')
@login_required
def myarticles(param):
    
    if param == 565678:
        return render_template('articles/565678.html')
    elif param == 565679:
        return render_template('articles/565679.html')
    elif param == 565680:
        return render_template('articles/565680.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()

        try:
            
            if user.username == username and check_password_hash(user.password, password):
                
                # Set cookie for user session
                set_session(
                    username=user.username
                )
                
                return redirect('/')
            else:
                flash('Login unsuccessful. Please check your username and password.', 'danger')
        except AttributeError:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():

    
    session.clear()
    session.permanent = False
    
    return redirect(url_for('login'), code=302)

if __name__ == '__main__':
    db.create_all()

    app.run()
