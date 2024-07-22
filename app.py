from flask import Flask, render_template, request, flash, redirect, url_for, session
from myuser_data import UserAuth

app = Flask(__name__)
app.secret_key = 'supersecretkey'
myuser_data=UserAuth()

@app.route("/")
def home():
  return render_template('index.html')

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

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Welcome {session['username']} to your dashboard!"
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('userName', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)