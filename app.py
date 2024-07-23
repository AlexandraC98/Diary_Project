from flask import Flask, render_template, request, flash, redirect, url_for, session
import myuser_data
import myentries


app = Flask(__name__)
app.secret_key = 'supersecretkey'


#Index Page - two choices will appear: to login or to register
@app.route("/")
def index():
  return render_template('index.html')


#Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['userName']
        password = request.form['userPassword']
        success, message = myuser_data.LoginUser(username, password)
        flash(message)
        if success:
            return redirect(url_for('dashboard'))
    return render_template('login.html')


#Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['userName']
        password = request.form['userPassword']
        success, message = myuser_data.AddUser(username, password)
        flash(message)
        if success:
            return redirect(url_for('dashboard'))
    return render_template('register.html')


#Diary Home
@app.route('/home')
def home():
    if 'username' in session:
        return f"Welcome {session['username']} to your home page!"
    return render_template('home.html')

#Add Entry
@app.route('/addentry')
def addentry():
    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['entry']
        # Add entry using the function from your original code
        myentries.add_entry(title, entry)
        return redirect(url_for('addentry'))
    return render_template('home.html')

#View Entry
@app.route('/viewentry')
def viewentry():
    if request.method == 'POST':
        next_entry = request.form['Next entry']
        previous_entry = request.form['Previous entry']
        myentries.view_entry(next_entry, previous_entry)
        return redirect(url_for('viewentry'))
    return render_template('home.html')


@app.route('/logout')
def logout():
    session.pop('userName', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)