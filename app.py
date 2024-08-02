from flask import Flask, render_template, request, flash, redirect, session # type: ignore
from dotenv import load_dotenv # type: ignore
import filesave
import hashlib
import random
import datetime
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

Diary, Users = filesave.AutoLoad()

app = Flask(__name__, static_url_path="/static")
app.secret_key = 'SECRET_KEY'


#Subroutine to hash and salt user information
def hash_with_salt(text, salt):
  return hashlib.sha256(f"{text}{salt}".encode()).hexdigest()


#Sort the entries according to the time they were submitted
def sorted_entries(current_user, Diary):
    if current_user not in Diary:
        return "No entries found for this user."
    
    entries = Diary[current_user]
    sorted_entries = sorted(entries, key=lambda x: x['timestamp'], reverse=True) #sort in reversed order, to see the latest entry

    content = ""
        
    for index, entry in enumerate(sorted_entries):
        local_time = datetime.datetime.now()
        formatted_entry = (f"{index+1}. {local_time.strftime('%Y-%m-%d %H:%M:%S')} \nTitle: {entry['title']} \nEntry: {entry['entry']}")
        content += formatted_entry
    
    filesave.AutoSave(Diary,Users)

    return content


#Index Page - two choices will appear: to login or to register
@app.route("/")
def index():

    if session.get('user'):
        return redirect ('/home') #if I'm logged in, don't make me login again
        
    return render_template('index.html')


#Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if session.get('user'):
        return redirect ('/home') #if I'm logged in, don't make me login again

    if request.method == 'POST':

        salt = str(random.randint(1000, 9999999999999)) # creating a random salt to add to the hashed username/password

        # post method to get user input
        username = request.form['userName']
        password = request.form['userPassword']

        # hashing username and password and adding salt at the end
        newUser = hash_with_salt (username, salt)
        newPass = hash_with_salt (password, salt)

        # check to see if the hashed and salted username already exists
        if newUser in Users:
            flash ("Username already exists.")
            return redirect ("/register")
        
        # if it's a new username, save the data in a dictionary and redirect the page to login
        Users[newUser] = {'password': newPass, 'salt': salt}
        filesave.AutoSave(Diary,Users)
        return redirect('/login')
        
    return render_template('register.html')


#Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if session.get('user'):
        return redirect ('/home') #if I'm logged in, don't make me login again
  
    if request.method == 'POST':

        # post method to get user input
        username = request.form['userName']
        password = request.form['userPassword']

        # for loop to get the salt which was generated for the stored_user and using it to hash and salt the input from the user
        for stored_user, user_data in Users.items():
            salt = user_data["salt"]
            newUser = hash_with_salt (username,salt)

            # check if newUser is stored in the dictionary; if it is, then hash and salt the password
            if newUser == stored_user:
                newPass = hash_with_salt (password,salt)

                # if the hashed password is equivalent to the stored password, then redirect to dashboard page
                if user_data['password'] == newPass:
                    session['user'] = {'username': username}
                    return redirect ('/home')

            flash ("Invalid username or password.")
            return redirect('/login')

    else:
        return redirect('login')


#Diary Home Page
@app.route('/home')
def home():

  if 'user' not in session: #if you're not logged in, then please do
    return redirect('/')
  
  current_user = session['user']['username']
  entries = sorted_entries[current_user][Diary]
  
  return render_template('home.html', entries=entries)
  

#Add Entry
@app.route('/addentry', methods = ["POST"])
def addentry():

    if session.get('user'):
        return redirect ('/home') #if I'm logged in, don't make me login again

    form = request.form

    entry = {
        "date": form["date"],
        "title": form["title"],
        "body": form["body"],
        "timestamp": datetime.datetime.now()
    }

    current_user = session['user']['username']
    if current_user not in Diary:
        Diary[current_user]=[]
    Diary[current_user].append(entry)
    filesave.AutoSave(Diary,Users)

    flash("Entry added successfully.")
    return redirect ('/home')


#View Entry
@app.route('/viewentry')
def viewentry():

    if session.get('user'):
        return redirect ('/home') #if I'm logged in, don't make me login again
    
    current_user = session['user']['username']
    entries = sorted_entries[current_user][Diary]

    return render_template ('view_entry.html', content = entries)


#Logout of App
@app.route('/logout')
def logout():

    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)