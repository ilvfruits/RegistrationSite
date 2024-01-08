from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置一个秘密密钥以启用会话

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    company_name = db.Column(db.String(120), nullable=True)
    logo_path = db.Column(db.String(200), nullable=True)


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['id']=user.id
            user_id = session.get('id')
            company_name = user.company_name
            company_logo = user.logo_path
            flash(f'{user_id} Login successful')
            return render_template('home.html', company_name=company_name, company_logo=company_logo)
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        company_name = request.form['company_name']
        logo = request.files['logo']

        if not username or not password:
            flash('Username and password are required.')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another username.')
        else:
            if logo and allowed_file(logo.filename):
                filename = secure_filename(logo.filename)
                logo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                new_user = User(username=username, password=password, company_name=company_name, logo_path=os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful. You can now login.')

                return redirect(url_for('login'))  # Redirect to the login page after successful registration

    return render_template('register.html')
    

@app.route('/change_company_info', methods=['GET', 'POST'])
@login_required
def change_company_info():
    if request.method == 'POST':
        user_id = session.get("id")
        user = User.query.get(user_id)

        company_name = request.form['company_name']
        logo = request.files['logo']

        if company_name:
            user.company_name = company_name

        if logo and allowed_file(logo.filename):
            filename = secure_filename(logo.filename)
            logo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))            
            user.logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)            
            db.session.commit()
            flash('Company information updated successfully')
        return render_template('home.html', company_name=user.company_name, company_logo=user.logo_path)
    return render_template('change_company_info.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)