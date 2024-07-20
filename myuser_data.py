import pwinput
import random
import hashlib
import os
import time
import filesave

Diary, Users = filesave.AutoLoad()

def AutoSave():
  filesave.AutoSave(Diary, Users)

#Subroutine to hash and salt user information
def hash_with_salt(text, salt):
  return hashlib.sha256(f"{text}{salt}".encode()).hexdigest()

###Storing user information
#Add diary user
def AddUser(Users, AutoSave):
  os.system("clear")

  salt = str(random.randint(1000, 9999999999999))

  username = input("Username: ")
  newUser = hash_with_salt(username, salt)

  if newUser in Users:

    print("User already exists.")
    time.sleep(1)

  else:

    password = pwinput.pwinput("Password: ")
    newPass = hash_with_salt(password, salt)

    Users[newUser] = {"password": newPass, "salt": salt}
    AutoSave()

  print()
  
  print("\033[35m User added. \033[0m")
  time.sleep(1)

#Login to your diary
def LoginUser(Users):
  os.system("clear")

  username = input("Username: ")

  for user, user_data in Users.items():

    salt = user_data["salt"]
    newUser = hash_with_salt(username, salt)

    if newUser == user:

      password = pwinput.pwinput("Password: ")
      newPass = hash_with_salt(password, salt)

      if newPass == user_data["password"]:

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