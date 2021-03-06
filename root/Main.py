import os
from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_login import UserMixin, LoginManager, login_required, current_user, login_user, logout_user, fresh_login_required

UPLOAD_FOLDER = '/static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'wmv', 'flv', 'avi' }

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = b'1\x96\x89\x16aR+JAr\xe1\xa8\x10ZI}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://lukeraunak:lukeraunak@127.0.0.1:3306/goldcheddardb'
app.permanent_session_lifetime = timedelta(minutes=30)


engine = create_engine(
 'mysql+mysqlconnector://lukeraunak:lukeraunak@127.0.0.1:3306/goldcheddardb'
)
Sesh = sessionmaker()

Sesh.configure(bind = engine)

sesh = Sesh()
connection = engine.connect()
connection = connection.execution_options(
    isolation_level="READ COMMITTED"
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.refresh_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return sesh.query(user).get(int(user_id))

@app.before_request
def before_request():
    session.permanent = True

#models

class posts(db.Model):
    id = db.Column (db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100))
    pub_date = db.Column(db.DateTime, nullable=False)
    author = db.Column(db.String(80))
    banner = db.Column(db.String(40))
    description = db.Column(db.String(256))
    content = db.Column(db.Text(4294000000), nullable=True)
    category = db.Column(db.String(100))
    read_count=db.Column(db.Integer, default = 0)
    def __repr__(self):
        return "<posts(title = {title}, pub_date = {pub_date}, author = {author}, banner = {banner}, description = {description}, content = {content})>".format(title = self.title, pub_date = self.pub_date, author = self.author, banner = self.banner, description = self.description, content = self.content)

class tag(db.Model):
    name = db.Column(db.String(25), primary_key = True, unique = True)
    def __repr__(self):
        return 'Tag {name}'.format(name = self.name)

class postTags(db.Model):
    tag = db.Column(db.String(25), db.ForeignKey('tag.name'), primary_key = True)
    post = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable = False)

class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(50), unique = True)
    passwordH = db.Column(db.String(128))
    def __repr__(self):
        return "<user(username = {username}, passwordH = b'{passwordH}')>".format(username = self.username, passwordH = self.passwordH)
    

#functions

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check(path2File):
    if os.path.isfile(path2File):
        return False
    else:
        return True

def valid_login(u, p):
    userQuery = sesh.query(user).filter_by(username = u).first()
    if userQuery != None:
        if bcrypt.check_password_hash(userQuery.passwordH, p):
            return True
    return False

def checkErr(u, p):
    userQuery = sesh.query(user).get(u)
    if userQuery != None:
        if bcrypt.check_password_hash(userQuery.passwordH, p):
            pass
        else:
            return 'Password Incorrect'
    else:
        return 'Username Incorrect'

def singup_validation(u, p, pc):
    if p == pc:
        userQuery = sesh.query(user).get(u)
        if userQuery == None:
            return True
    return False

def checkErrSU(u, p, pc):
    if p != pc:
        return 'Passwords Do not match'
    userQuery = sesh.query(user).get(u)
    if userQuery != None:
        return 'Username Taken'

# user accessable pages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/moneyManagement')
def moneyManagment():
    return render_template('moneyManagement.html')

@app.route('/moneyManagement/investing')
def investing():
   return render_template('investing.html')

@app.route('/moneyManagement/investing/stocks')
def method_name():
    today = datetime.date.today()
    allposts = posts.query.filter(posts.pub_date <= today, posts.category == 'stocks')
    return render_template('stocks.html', allposts = allposts)

@app.route('/moneyManagement/investing/stocks/<postId>')
def stockPosts(postId):
    post = sesh.query(posts).filter(posts.id == postId).first()
    return render_template('post.html', post = post)

@app.route('/incomeGrowth')
def incomeGrowth():
   return render_template('incgrow.html')

@app.route('/incomeGrowth/passiveIncome')
def passiveIncome():
    today = datetime.date.today()
    allposts = posts.query.filter(posts.pub_date <= today, posts.category == 'passiveinc')
    return render_template('passiveinc.html', allposts = allposts)

@app.route('/incomeGrowth/passiveIncome/<postId>')
def passiveincPosts(postId):
    post = sesh.query(posts).filter(posts.id == postId).first()
    return render_template('post.html', post = post)

@app.route('/incomeGrowth/activeIncome')
def activeIncome():
    today = datetime.date.today()
    allposts = posts.query.filter(posts.pub_date <= today, posts.category == 'activeinc')
    return render_template('activeinc.html', allposts = allposts)

@app.route('/incomeGrowth/activeIncome/<postId>')
def activeincPosts(postId):
    post = sesh.query(posts).filter(posts.id == postId).first()
    return render_template('post.html', post = post)

@app.route('/incomeGrowth/incgrowth')
def incgrowth():
    today = datetime.date.today()
    allposts = posts.query.filter(posts.pub_date <= today, posts.category == 'incgrowth')
    return render_template('incgrowposts.html', allposts = allposts)

@app.route('/incomeGrowth/incgrowth/<postId>')
def incgrowPosts(postId):
    post = sesh.query(posts).filter(posts.id == postId).first()
    return render_template('post.html', post = post)

# admin pages

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            u = sesh.query(user).filter_by(username = request.form['username']).first()
            login_user(u)
            return redirect(url_for('admin'))
        error = checkErr(request.form['username'], request.form['password'])
    return render_template('login.html', error = error)

@app.route('/admin', methods = ['GET', 'POST'])
@fresh_login_required
def admin():
    uQuery = sesh.query(user).all()
    allposts = posts.query.all()
    list = []
    if request.method == 'POST' and request.form['type'] == 'addUser':
        if singup_validation(request.form['username'], request.form['password'], request.form['passwordConf']):
            passH = bcrypt.generate_password_hash(request.form['password'], 10).decode('utf-8')
            newUser = user(username = request.form['username'], passwordH = passH)
            sesh.add(newUser)
            sesh.commit()
            return redirect(url_for('admin'))
        else:
            error = checkErrSU(request.form['username'], request.form['password'], request.form['passwordConf'])
            return render_template('adminHome.html', users = uQuery, error = error )
    if request.method == 'POST' and request.form['type'] == 'post':
        f = request.files
        if request.form['formType'] == 'text':
            f = f['banner']
            filename = secure_filename(f.filename)
            if f and allowed_file(f.filename) and check('static/uploads/' + filename):
                f.save('static/uploads/' + filename)
            banner = 'uploads/' + filename
            f = request.files['imagein']
            filename = secure_filename(f.filename)
            if f and allowed_file(f.filename) and check('static/uploads/' + filename):
                f.save('static/uploads/' + filename)
            image = '/static/uploads/'+ filename
            content = '<p>' + request.form['p1'] + '</p>' + '<img id = "img1" src = "' + image + '">'
            x = 1
            y = 0
            for i in request.form.items():
                x += 1
            x -=9
            if x != 0:
                pnum = 2
                while y < x:
                    pnum = str(pnum)
                    ind = 'p' + pnum
                    content += '<p>' + request.form[ind] + '</p>'
                    y += 1
                    pnum = int(pnum)
                    pnum += 1
        if request.form['formType'] == 'vid':
            f = f['banner']
            filename = secure_filename(f.filename)
            if f and allowed_file(f.filename) and check('static/uploads/' + filename):
                f.save('static/uploads/' + filename)
            banner = 'uploads/' + filename
            f = request.files['video']
            filename = secure_filename(f.filename)
            if f and allowed_file(f.filename) and check('static/uploads/' + filename):
                f.save('static/uploads/' + filename)
            video = 'uploads/' + filename
            content_type = filename.rsplit('.')[-1].lower()
            content = '<p>' + request.form['p1'] + '</p>' + '<video id = "vid" controls> <source type = "video/'+ content_type + '" src = "' + video + '">'
        if request.form['formType'] == 'dyn':
            f = f['banner']
            filename = secure_filename(f.filename)
            if f and allowed_file(f.filename) and check('static/uploads/' + filename):
                f.save('static/uploads/' + filename)
            banner = 'uploads/' + filename
            x = 1
            y = 1
            iNum = 1
            vNum = 1
            for i in request.form.items():
                x += 1
            for f in request.files.items():
                y += 1
            content = ''
            if x > 0:
                for m in request.form:
                    if 'pD' in m:
                        content += '<p id = "' + m + '">' + request.form[m] + '</p>'
            if y > 0:
                for m in request.files:
                    if m != 'banner':
                        s = request.files[m]
                        filename = secure_filename(s.filename)
                        if s and allowed_file(s.filename) and check('static/uploads/' + filename):
                            s.save('static/uploads/' + filename)
                        if 'i' in m:
                            image = '/static/uploads/' + filename
                            content += '<img id = "' + m + '" src = "' + image + '">'
                        if 'v' in m:
                            video = '/static/uploads/' + filename
                            content_type = filename.rsplit('.')[-1].lower()
                            content += '<video id = "' + m + '" controls> <source type = "video/'+ content_type + '" src = "' + video + '">'
        if content == '':
            return redirect(url_for('admin'))
        newPost = posts(title = request.form['title'], pub_date = request.form['pubDate'], author = request.form['author'], banner = banner, description =  request.form['description'], content = content, category = request.form['category'], read_count = 0)
        sesh.add(newPost)
        sesh.commit()
    return render_template('adminHome.html', users = uQuery, allposts = allposts)

@app.route('/admin/posts/<postId>')
@login_required
def postView(postId):
    post = sesh.query(posts).filter(posts.id == postId).first()
    return render_template('postView.html', post = post)

@app.route('/admin/posts/<postId>/delete')
@login_required
def postDelete(postId):
    post = sesh.query(posts).get(postId)
    sesh.delete(post)
    sesh.commit()
    return redirect(url_for('admin'))

@app.route('/admin/users/remove/<username>')
@login_required
def removeUser(username):    
    u = sesh.query(user).filter(user.username == username).first()
    sesh.delete(u)
    sesh.commit()
    return(redirect(url_for('logout')))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
