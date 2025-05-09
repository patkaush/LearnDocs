# test_db.py
from DbHandler import init_db

try:
    init_db()
    print("successful!")

except Exception as e:
    print("Error:", e)
