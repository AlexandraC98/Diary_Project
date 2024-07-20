import pytz
import os
import filesave
import myuser_data
import myentries

#Exact date and time of my current location, Bucharest
bucharest_tz = pytz.timezone('Europe/Bucharest')

def AutoSave():
  filesave.AutoSave(Diary, Users)

Diary, Users = filesave.AutoLoad()

#Exit the diary
def Quit():
  choice=input("Do you want to go back to the menu? (y/n) ")
  if choice.lower().startswith("n"):
    filesave.AutoSave(Diary, Users)
    return True
  return False

#Main Loop: add/login, then store/remove/view entries to your user
current_user=None

while True:
  os.system("clear")
  menu1=input("1. Add user\n\n2. Login to your diary\n\n> ")

  if menu1=="1":
    myuser_data.AddUser(Users, AutoSave)
  elif menu1=="2":
    current_user=myuser_data.LoginUser(Users)
    
    if current_user:
    
      while True:
        os.system("clear")
        menu=input("1. Add entry\n\n2. View entry\n\n3. Remove entry\n\n> ")
        if menu=="1":
          myentries.add_entry(current_user, AutoSave)
        elif menu=="2":
          myentries.view_entry(current_user, Diary)
        elif menu=="3":
          myentries.remove_entry(current_user, Diary, AutoSave)
  
        if Quit():
          break

  user_input=input("Do you want to exit? (y/n) ")
  if user_input.lower().startswith("y"):
    break