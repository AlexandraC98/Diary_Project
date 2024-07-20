import json
import datetime

Diary={}
Users={}

#Auto-load: load the user information and the entries which were stored in Diary.txt and add more data
def AutoLoad():
  try:
    with open("Diary.txt", "r") as f:
      data = json.load(f)
      # Convert string keys back to datetime objects
      Diary = {user: [{"title": entry["title"], "entry": entry["entry"], "timestamp": datetime.datetime.fromisoformat(entry["timestamp"])} for entry in entries] for user, entries in data.get("Entries", {}).items()}
      Users = data.get("Users", {})
      return Diary, Users
  except Exception:
    return {}, {}

#Auto-save: store the new information in Diary.txt
def AutoSave(Diary, Users):
  with open("Diary.txt", "w") as f:
    # Convert datetime keys to strings for JSON serialization
    data = {
    "Entries": {user: [{"title": entry["title"], "entry": entry["entry"], "timestamp": entry["timestamp"].isoformat()} for entry in entries] for user, entries in Diary.items()},
    "Users": Users}
    json.dump(data,f)