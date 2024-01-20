from flask import Flask,render_template,request, redirect, url_for
# from jinja2 import template
from model import db,User as user_model,Section

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
        username = request.form['username']
        c = user_model.query.filter_by(email=email).first()
        print("sign",c)
        if c:
            return render_template('DashBoard.html',email=email,passw=passw)
        else:
            info ="hey there"
            user=user_model(email=email,password=passw,role="admin",username=username)
            db.session.add(user)
            db.session.commit()
            return render_template('login.html',info=info)        
        
@app.route('/dash', methods=["GET"])
def dash():
    users1 = user_model.query.all()
    data = Section.query.all()
    return render_template('DashBoard.html',users=users1, data=data)

@app.route('/upload/section/<int:user_id>', methods=['GET','POST'])
def upload_section(user_id):
    if request.method == 'GET':
        return render_template('upload_section.html',id=user_id)
    if request.method == 'POST':
        name = request.form['sec_name']
        desc = request.form['sec_description']
        new_section = Section( sec_name=name, sec_description=desc,user_id=user_id)

        db.session.add(new_section)
        db.session.commit()
        return redirect(url_for('dash'))


    # return render_template('upload_section.html',id=id)

@app.route('/update/section/<int:sec_id>', methods=['GET','POST'])
def update_section(sec_id):
    if request.method == 'GET':
        return render_template('update_section.html',id=sec_id)
    if request.method == 'POST':
        name = request.form['sec_name']
        Section.query.filter_by(id=sec_id).update({Section.sec_name: name})

        # print(db.session.update(Section,sec_id))
        # print(Section.query.filter_by(id=sec_id))
        # new_section = Section( sec_name=name)

        # db.session.add(new_section)
        db.session.commit()
        return redirect(url_for('dash'))
    return render_template('update_section.html',id=sec_id)

@app.route('/delete/section/<int:sec_id>', methods=['GET','POST'])
def delete_section(sec_id):
    section = Section.query.get_or_404(sec_id)
        # Section.query.filter_by(id=sec_id).delete({Section.sec_name: name})
    db.session.delete(section)
        # db.session.add(new_section)
    db.session.commit()
    return redirect(url_for('dash'))
    # return render_template('DashBoard.html')

# @app.route('/search/<string:name>', methods=["GET"])  
# def search(name):
#     data = Section.query.all()
#     if name1 in data:
#         name1 = name
#         return render_template('search.html')
#     else:
#         return render_template('error.html')
#     # return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
    