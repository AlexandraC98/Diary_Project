import datetime, pytz, os, time, pwinput

bucharest_tz = pytz.timezone('Europe/Bucharest')

Diary={}

real_psw="AlexandraC98"

#Auto-load
try:
  with open("Diary.txt", "r") as f:
    Diary=eval(f.read())
except Exception:
  pass

#Printing option
def printDiary():
  sorted_keys = sorted(Diary.keys(), reverse=True)
  for index, key in enumerate(sorted_keys):
    local_time = key.astimezone(bucharest_tz)
    print(f"{index+1}. {local_time.strftime('%Y-%m-%d %H:%M:%S')} > {Diary[key]['title']}")
  print()

#Add entry
def Add():
  os.system("clear")
  title=input("Title > ").capitalize()
  entry=input("Entry > ")
  key=datetime.datetime.now(pytz.utc)
  Diary[key]={"title":title,"entry":entry}
  print("Entry added.")
  time.sleep(1)

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
  
    choice=input(f"1. Next entry\n2. Previous entry\n3. Exit\n> ")

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
      print(f"Entry deleted.")
      print()
      printDiary()
      time.sleep(1)

  except ValueError:
    print("Invalid input. Please enter a number.")
    time.sleep(1)

#Auto-save
def AutoSave():
  with open("Diary.txt", "w") as f:
    f.write(str(Diary))

#Exit the diary
def Quit():
  choice=input("Do you want to go back to the menu? (y/n) ")
  if choice.lower().startswith("n"):
    AutoSave()
    return True
  return False

while True:
  os.system("clear")
  psw=pwinput.pwinput("Enter your password: ")
  if psw!=real_psw:
    break
  else:
    while True:
      os.system("clear")
      menu=input("1. Add entry\n2. View entry\n3. Remove entry\n> ")
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
