import os

if os.path.exists("test.db"):
    print("Database file exists")
else:
    print("Database file does not exist")