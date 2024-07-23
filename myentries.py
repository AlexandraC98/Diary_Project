import os
import time
import datetime
import pytz
import filesave

Diary = {}
Users = filesave.AutoLoad()

#Exact date and time of my current location, Bucharest
bucharest_tz = pytz.timezone('Europe/Bucharest')

#Printing option: for each user, print the indexed title and entry for the exact date in which they were written
def printDiary(current_user, Diary):
  if current_user in Diary:
    entries = Diary[current_user]
    sorted_keys = sorted(entries, key=lambda x: x['timestamp'], reverse=True)
      
  for index, entry in enumerate(sorted_keys):
    local_time = entry['timestamp'].astimezone(bucharest_tz)
    print(f"{index+1}. {local_time.strftime('%Y-%m-%d %H:%M:%S')} \nTitle: {entry['title']} \nEntry: {entry['entry']}")
      
  print()


def AutoSave():
  filesave.AutoSave(Diary, Users)

###Entries
#Add entry
def add_entry(current_user, AutoSave):
  os.system("clear")
    
  title=input("Title > ").capitalize()
  entry=input("Entry > ").capitalize()
  key=datetime.datetime.now(pytz.utc)

  if current_user not in Diary:
    Diary[current_user] = []

  Diary[current_user].append({"title": title, "entry": entry, "timestamp": key})
    
  print("Entry added.")
  time.sleep(1)

  AutoSave()

#View entry
def view_entry(current_user, Diary):
  sorted_entries=[]

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
      index=(index-1)
      if index < 0:
        index = len(sorted_entries) - 1  # Wrap around to the last entry
    elif choice=="2":
      index=(index+1)
      if index >= len(sorted_entries):
        index = 0  # Wrap around to the first entry
    elif choice=="3":
      break
    else:
      print("Invalid choice. Please try again.")
      time.sleep(1)

#Remove entry
def remove_entry(current_user, Diary, AutoSave):
  os.system("clear")

  printDiary(current_user, Diary)

  try:
    user_index=int(input("Which entry do you wish to remove? > ")) - 1

    if user_index<0 or user_index>len(Diary.get(current_user, [])):
      print("Invalid index. Please enter the correct index.")

    else:
      sorted_entries = sorted(Diary[current_user], key=lambda x: x['timestamp'], reverse=True)
      entry_to_remove = sorted_entries[user_index]

      # Find the exact entry in the original list
      for entry in Diary[current_user]:
        if entry['timestamp'] == entry_to_remove['timestamp']:
          Diary[current_user].remove(entry)

      print("Entry deleted.")

      time.sleep(1)
      os.system("clear")

      printDiary(current_user, Diary)

      time.sleep(1)

      AutoSave()

  except ValueError:
    print("Invalid input. Please enter a number.")
    time.sleep(1)