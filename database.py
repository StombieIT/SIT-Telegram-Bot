import sqlite3
class DataBase(sqlite3.Connection):
	def __init__(self, filename):
		'''
		filename serves as the name of file of your
		database when you initialize creating object
		of this class
		'''
		self.filename = filename
		self.db = sqlite3.Connection(self.filename)
		self.cursor = self.db.cursor()
	def create(self, table, **kwargs):
		'''
		table is the name of table which you want to
		create
		kwargs is arguments in which key serves as
		the name of var and the value of it serves
		as type of it
		'''
		var = ["{} {}".format(key.strip(), value.strip().upper()) for key, value in kwargs.items()]
		self.cursor.execute("CREATE TABLE IF NOT EXISTS {t}({v})".format(t=table, v=', '.join(var)))
		self.db.commit()
	def delete(self, table):
		'''
		table is the name of table you want to delete
		'''
		self.cursor.execute("DROP TABLE {t}".format(t=table))
		self.db.commit()
	def log(self, table, **kwargs):
		'''
		table is the name of table you want to use
		kwargs is arguments in which key serves as
		name in which you want to log something and
		the value of it serves as value you want to log
		'''
		keys = []
		for key in kwargs.keys():
			keys.append(key.strip())
		values = []
		for value in kwargs.values():
			values.append(value.strip())
		self.cursor.execute("INSERT INTO {t} ({k}) VALUES ({v})".format(t=table, k=', '.join(keys), v=', '.join(values)))
		self.db.commit()
	def search(self, table, **kwargs):
		'''
		table is the name of table you want to use
		kwargs is argument in which key serves as
		name of var and the value of it serves as
		condition of searching
		'''
		assert len(kwargs) == 1
		for var, crit in kwargs.items():
			self.cursor.execute("SELECT * FROM {t} WHERE {v} {c}".format(t=table, v=var.strip(), c=crit.strip()))
			break
		for request in self.cursor.fetchall():
			yield request
	def search_with_and(self, table, **kwargs):
		'''
		table is the name of table you want to use
		kwargs is arguments in which key serves as
		name of var and the value of it serves as
		condition of searching with using operator 'AND'
		between conditions
		'''
		assert len(kwargs) > 1
		crit = ["{v} {c}".format(v=key.strip(), c=value.strip()) for key, value in kwargs.items()]
		self.cursor.execute("SELECT * FROM {t} WHERE {c}".format(t=table, c=' AND '.join(crit)))
		for request in self.cursor.fetchall():
			yield request
	def search_with_or(self, table, **kwargs):
		'''
		table is the name of table you want to use
		kwargs is arguments in which key serves as
		name of var and the value of it serves as
		condition of searching with using operator 'OR'
		between conditions
		'''
		assert len(kwargs) > 1
		crit = ["{v} {c}".format(v=key.strip(), c=value.strip()) for key, value in kwargs.items()]
		self.cursor.execute("SELECT * FROM {t} WHERE {c}".format(t=table, c=' OR '.join(crit)))
		for request in self.cursor.fetchall():
			yield request
