from pysqlcipher3 import dbapi2 as sqlcipher


class Database(object):
	__DB_PATH = "password_manager.db"

	def __init__(self, master_pass):
		self.db = sqlcipher.connect(__DB_PATH)
		self.db.execute(f"PRAGMA key='{master_pass}';")

	def is_master_pass_created(self):
		try:
			self.db.execute(
					"SELECT name FROM sqlite_master WHERE type='table' AND name='Password';"
				)
			return False
		except sqlcipher.DatabaseError:
			return True

	def is_master_pass_input_correct(self, master_pass_input):
		with self.db:
			try:
				self.db.execute(f"PRAGMA key='{master_pass_input}';")
				self.db.execute("SELECT count(*) FROM sqlite_master;")
				return True
			except sqlcipher.DatabaseError:
				return False
	
	

		