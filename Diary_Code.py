import datetime, pytz, os, time, pwinput, random, hashlib, json

bucharest_tz = pytz.timezone('Europe/Bucharest')

Diary={}
Users={}

#Auto-load
try:
  with open("Diary.txt", "r") as f:
    data = json.load(f)
    # Convert string keys back to datetime objects
    Diary = {datetime.datetime.fromisoformat(k): v for k, v in data.get("Entries", {}).items()}
    Users = data.get("Users", {})
except Exception:
  pass

#Auto-save
def AutoSave():
  with open("Diary.txt", "w") as f:
    # Convert datetime keys to strings for JSON serialization
    data = {
      "Entries": {k.isoformat(): v for k, v in Diary.items()},
      "Users": Users}
    json.dump(data,f)

#Printing option
def printDiary():
  sorted_keys = sorted(Diary.keys(), reverse=True)
  for index, key in enumerate(sorted_keys):
    local_time = key.astimezone(bucharest_tz)
    print(f"{index+1}. {local_time.strftime('%Y-%m-%d %H:%M:%S')} > {Diary[key]['title']}")
  print()

###Entries
#Add entry
def Add():
  os.system("clear")
  title=input("Title > ").capitalize()
  entry=input("Entry > ")
  key=datetime.datetime.now(pytz.utc)
  Diary[key]={"title":title,"entry":entry}
  print("Entry added.")
  time.sleep(1)
  AutoSave()

#View entry
def View():
  sorted_keys=sorted(Diary.keys(), reverse=True)
  if not sorted_keys:
    print("No entries found.")
    return

  index=0

  while True:
    os.system("clear")
    local_time=sorted_keys[index].astimezone(bucharest_tz)
    print(f"{local_time.strftime('%Y-%m-%d')}: {Diary[sorted_keys[index]]}", end="\n")
    time.sleep(1)

    choice=input("1. Next entry\n2. Previous entry\n3. Exit\n> ")

    if choice=="1":
      index=(index-1)
    elif choice=="2":
      index=(index+1)
    elif choice=="3":
      break
    else:
      print("Invalid choice. Please try again.")

#Remove entry
def Remove():
  os.system("clear")

  printDiary()

  try:
    user_index=int(input("Which entry do you wish to remove? > ")) - 1

    if user_index<0 or user_index>=len(Diary):
      print("Invalid index. Please enter the correct index.")

    else:
      removed_key = sorted(Diary.keys(), reverse=True)[user_index]
      del Diary[removed_key]
      print("Entry deleted.")
      print()
      printDiary()
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

    if newUser in Users:
      password = pwinput.pwinput("Password: ")
      newPass = hash_with_salt(password, salt)

      if newPass == Users[newUser]["password"]:
        print("\033[35m Login Successful. \033[0m")
        time.sleep(1)
        return True
      else:
         print("Login Failed")
         return False

  print("\033[33m Username not found. \033[0m")
  time.sleep(1)
  exit()

#Main Loop
while True:
  os.system("clear")
  menu1=input("1. Add user\n\n2. Login to your diary\n\n> ")

  if menu1=="1":
    AddUser()
  elif menu1=="2":
    if LoginUser():
    
      while True:
        os.system("clear")
        menu=input("1. Add entry\n\n2. View entry\n\n3. Remove entry\n\n> ")
        if menu=="1":
          Add()
        elif menu=="2":
          View()
        elif menu=="3":
          Remove()
  
        if Quit():
          break

  user_input=input("Do you want to exit? (y/n) ")
  if user_input.lower().startswith("y"):
    break