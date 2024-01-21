from flask import Flask, render_template, request, redirect, url_for, session, flash
from model import db, User as user_model, Section

app = Flask(__name__)
app.secret_key = "workshop-secret-key"
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize the extension
app.config.from_object(__name__)
from flask_session import Session
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db1.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.app_context().push()

with app.app_context():
    db.create_all()



# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = user_model.query.filter_by(email=email).first()
        print(user)
        # print(user.check_password(password))
        if user and user.role == 'admin':
            print(user.role)
            session['user_id'] = user.id
            flash('Login successful', 'success')
            return redirect(url_for('dash'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
            return render_template('login.html')

# Signup route
@app.route('/')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        existing_user = user_model.query.filter_by(email=email).first()

        if existing_user:
            flash('User with this email already exists. Please login.', 'warning')
            return redirect(url_for('signup'))
        else:
            new_user = user_model(email=email, password_hash=password, role="admin", username=username)
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful. Please login.', 'success')
            return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logout successful', 'success')
    return redirect(url_for('login'))

# Dashboard route
@app.route('/dash', methods=["GET"])
def dash():
    users1 = user_model.query.all()
    data = Section.query.all()
    return render_template('DashBoard.html', users=users1, data=data)

# Create Section route
@app.route('/create/section', methods=['GET', 'POST'])
def create_section():
    if request.method == 'GET':
        return render_template('create_section.html')
    elif request.method == 'POST':
        name = request.form['sec_name']
        desc = request.form['sec_description']
        # Get the user ID from the session
        user_id = session.get('user_id')
        
        new_section = Section(sec_name=name, sec_description=desc, user_id=user_id)

        db.session.add(new_section)
        db.session.commit()
        flash('Section created successfully', 'success')
        return redirect(url_for('dash'))

# Update Section route
@app.route('/update/section/<int:sec_id>', methods=['GET', 'POST'])
def update_section(sec_id):
    if request.method == 'GET':
        section = Section.query.get_or_404(sec_id)
        return render_template('update_section.html', section=section)
    elif request.method == 'POST':
        name = request.form['sec_name']
        desc = request.form['sec_description']
        
        Section.query.filter_by(id=sec_id).update({
            Section.sec_name: name,
            Section.sec_description: desc
        })

        db.session.commit()
        flash('Section updated successfully', 'success')
        return redirect(url_for('dash'))

# Delete Section route
@app.route('/delete/section/<int:sec_id>', methods=['POST'])
def delete_section(sec_id):
    section = Section.query.get_or_404(sec_id)
    db.session.delete(section)
    db.session.commit()
    flash('Section deleted successfully', 'success')
    return redirect(url_for('dash'))

# Search route
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        results = Section.query.filter(Section.sec_name.like(f"%{search_term}%")).all()
        return render_template('search_results.html', results=results)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
