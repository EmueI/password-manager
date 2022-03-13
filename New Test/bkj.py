from pysqlcipher3 import dbapi2 as sqlcipher

db = sqlcipher.connect("New Test/passwordManager.db")

db.execute('PRAGMA key="password";')
is_master_password_created = db.execute("PRAGMA key;").fetchall()

print(is_master_password_created)
