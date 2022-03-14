import sys
from os import system
from pysqlcipher3 import dbapi2 as sqlcipher


db = sqlcipher.connect("New Test/testing.db")
# # db.execute('PRAGMA key="abc123"')
# db.execute(
#     """
#     CREATE TABLE IF NOT EXISTS Passwords (
#     id INTEGER PRIMARY KEY,
#     name TEXT,
#     username TEXT,
#     password TEXT,
#     isCompromised INTEGER,
#     passwordStrength TEXT
#     );
#     """
# )
db.close()

db = sqlcipher.connect("New Test/testing.db")
is_table_created = len(db.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='Passwords';"
).fetchall()) > 0
print(is_table_created)
# db.execute(
#     """
#     INSERT INTO Passwords
#     VALUES (:id, :name, :username, :password, :isCompromised, :passwordStrength)
#     """,
#     {
#         "id": 0,
#         "name": "Discord",
#         "username": "jeffery",
#         "password": "ashfkjashf",
#         "isCompromised": 1,
#         "passwordStrength": "weak",
#     },
# )

# db = sqlcipher.connect("testing.db")
# db.execute(
#     f'PRAGMA key={"abc123"}',
# )
# try:
#     db.execute("SELECT count(*) FROM sqlite_master;")
# except sqlcipher.DatabaseError:
#     print("Incorrect password")
# db.close()
