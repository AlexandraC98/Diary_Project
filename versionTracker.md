## Version Tracker

**First commit**
- raw code with unique password given by me

**Second commit**
- added a second dictionary to save user infos
- created subroutines for adding new users and login function

**Third commit**
- fixed bugs in order to save entries for specific users, view and remove the entries of one user

**Fourth commit**
- started working in VSCode instead of Replit
- created function to verify if username already exists
- created separate files for a cleaner code:
    - subroutines for storing data
    - subroutines for user add and login functions
    - subroutines for adding, viewing, removing entries
    - main loop
- fixed removal of correct entry according to user input
- managed filesave functions in order to properly store data and import it in all files
- issues to be addressed: list index out of range within view_entry subroutine

**Fifth commit**
- created new branch for Flask implementation
- created app.py and pages for home, login and user registration
- installed python-dotenv using pip and created a ".flaskenv" in root directory, but kept getting error while trying to run flask; probably error with virtual environment (?)