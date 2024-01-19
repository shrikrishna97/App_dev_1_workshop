from flask import Flask,render_template,request, redirect, url_for
# from jinja2 import template
from model import db,User as user_model

app = Flask(__name__)
app.secret_key = "workshop-secret-key"

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db1.sqlite3'

db.init_app(app)

app.app_context().push()

with app.app_context():
    db.create_all()

# ctrl + /
@app.route('/')
def index():
    greet = '<h1>Hello, Gators!</h1>'
    link = '<p><a href="user/Albert">Click me!</a></p>'
    return greet + link
    # return '<h1>hello workshop</h1> <h6>hello workshop</h6>, '

@app.route('/user/<int:name>')
def user(name):
    personal = f'<h1>Hello, {name}!</h1>'
    # above - the curly braces {} hold a variable; when this runs,
    # the value will replace the braces and the variable name
    instruc = '<p>Change the name in the <em>browser address bar</em> \
        and reload the page.</p>'
    return personal + instruc

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        email = request.form['email']
        passw = request.form['password']

        c = user_model.query.filter_by(email=email)
        print(c)
        if c:
            return render_template('DashBoard.html',email=email,passw=passw)
        else:
            return render_template('login.html')
        
@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    elif request.method=='POST':
        email = request.form['email']
        passw = request.form['password']

        c = user_model.query.filter_by(email=email).first()
        print("sign",c)
        if c:
            return render_template('DashBoard.html',email=email,passw=passw)
        else:
            info ="hey there"
            user=user_model(email=email,password=passw)
            db.session.add(user)
            db.session.commit()
            return render_template('login.html',info=info)        
        
@app.route('/dash', methods=["GET"])
def dash():
    users1 = user_model.query.all()
    return render_template('DashBoard.html',users=users1)       

if __name__ == '__main__':
    app.run(debug=True)
    