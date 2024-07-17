import datetime, pytz, os, time, pwinput, random, hashlib, json

bucharest_tz = pytz.timezone('Europe/Bucharest')

Diary={}
Users={}

#Auto-load
try:
  with open("Diary.txt", "r") as f:
    data = json.load(f)
    # Convert string keys back to datetime objects
    Diary = {user: [{"title": entry["title"], "entry": entry["entry"], "timestamp": datetime.datetime.fromisoformat(entry["timestamp"])} for entry in entries] for user, entries in data.get("Entries", {}).items()}
    Users = data.get("Users", {})
except Exception:
  pass

#Auto-save
def AutoSave():
  with open("Diary.txt", "w") as f:
    # Convert datetime keys to strings for JSON serialization
    data = {
    "Entries": {user: [{"title": entry["title"], "entry": entry["entry"], "timestamp": entry["timestamp"].isoformat()} for entry in entries] for user, entries in Diary.items()},
    "Users": Users}
    json.dump(data,f)

#Printing option
def printDiary(current_user):
  if current_user in Diary:
    entries = Diary[current_user]
    sorted_keys = sorted(entries, key=lambda x: x['timestamp'], reverse=True)
    
  for index, entry in enumerate(sorted_keys):
    local_time = entry['timestamp'].astimezone(bucharest_tz)
    print(f"{index+1}. {local_time.strftime('%Y-%m-%d %H:%M:%S')} > Title: {entry['title']}\nEntry: {entry['entry']}")
    
  print()

###Entries
#Add entry
def Add(current_user):
  os.system("clear")
  
  title=input("Title > ").capitalize()
  entry=input("Entry > ")
  key=datetime.datetime.now(pytz.utc)

  if current_user not in Diary:
    Diary[current_user] = []

  Diary[current_user].append({"title": title, "entry": entry, "timestamp": key})
  
  print("Entry added.")
  time.sleep(1)
  AutoSave()

#View entry
def View(current_user):
  if current_user in Diary:
    sorted_entries = sorted(Diary[current_user], key=lambda x: x['timestamp'], reverse=True)
    if not sorted_entries:
      print("No entries found.")
      time.sleep(1)
      return

  index=0

  while True:
    os.system("clear")
    local_time=sorted_entries[index]['timestamp'].astimezone(bucharest_tz)
    print(f"{local_time.strftime('%Y-%m-%d %H:%M:%S')}: Title: {sorted_entries[index]['title']}\nEntry: {sorted_entries[index]['entry']}\n")
    time.sleep(1)

    choice=input("1. Next entry\n2. Previous entry\n3. Exit\n> ")

    if choice=="1":
      index=(index-1) % len(sorted_entries)
    elif choice=="2":
      index=(index+1) % len(sorted_entries)
    elif choice=="3":
      break
    else:
      print("Invalid choice. Please try again.")
      time.sleep(1)

#Remove entry
def Remove(current_user):
  os.system("clear")

  printDiary(current_user)

  try:
    user_index=int(input("Which entry do you wish to remove? > ")) - 1

    if user_index<0 or user_index>=len(Diary.get(current_user, [])):
      print("Invalid index. Please enter the correct index.")

    else:
      removed_entry = Diary[current_user].pop(user_index)
      print("Entry deleted.")
      time.sleep(1)
      os.system("clear")
      printDiary(current_user)
      time.sleep(1)
      AutoSave()

  except ValueError:
    print("Invalid input. Please enter a number.")
    time.sleep(1)

#Exit the diary
def Quit():
  choice=input("Do you want to go back to the menu? (y/n) ")
  if choice.lower().startswith("n"):
    AutoSave()
    return True
  return False

#Subroutine to hash and salt
def hash_with_salt(text, salt):
  return hashlib.sha256(f"{text}{salt}".encode()).hexdigest()

###Users
#Add diary user
def AddUser():
  os.system("clear")
  username = pwinput.pwinput("Username: ")
  password = pwinput.pwinput("Password: ")

  salt = str(random.randint(1000, 9999999999999))

  newUser = hash_with_salt(username, salt)
  newPass = hash_with_salt(password, salt)

  Users[newUser] = {"password": newPass, "salt": salt}

  print()
  
  print("\033[35m User added. \033[0m")
  time.sleep(1)
  
  AutoSave()

#Login to your diary
def LoginUser():
  os.system("clear")
  username = pwinput.pwinput("Username: ")

  for user in Users:
    salt = Users[user]["salt"]
    newUser = hash_with_salt(username, salt)

    if newUser == user:
      password = pwinput.pwinput("Password: ")
      newPass = hash_with_salt(password, salt)

      if newPass == Users[newUser]["password"]:
        print("\033[35m Login Successful. \033[0m")
        time.sleep(1)
        return user
      else:
        print("Login Failed")
        time.sleep(1)
        return None

  print("\033[33m Username not found. \033[0m")
  time.sleep(1)
  exit()

#Main Loop
current_user=None

while True:
  os.system("clear")
  menu1=input("1. Add user\n\n2. Login to your diary\n\n> ")

  if menu1=="1":
    AddUser()
  elif menu1=="2":
    current_user=LoginUser()
    
    if current_user:
    
      while True:
        os.system("clear")
        menu=input("1. Add entry\n\n2. View entry\n\n3. Remove entry\n\n> ")
        if menu=="1":
          Add(current_user)
        elif menu=="2":
          View(current_user)
        elif menu=="3":
          Remove(current_user)
  
        if Quit():
          break

  user_input=input("Do you want to exit? (y/n) ")
  if user_input.lower().startswith("y"):
    break