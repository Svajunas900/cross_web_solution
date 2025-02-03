import sqlite3

class SqliteConnection:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls, *args, **kwargs)
      cls._instance.connection = sqlite3.connect("django_comp_db.sqlite3")
      cls._instance.cursor = cls._instance.connection.cursor()
      return cls._instance
  
  def fetch_data(self, query: str) -> list:
    self.cursor.execute(query)
    return self.cursor.fetchall()
  
  def save_data(self, query: str, values: str) -> None:
    self.cursor.executemany(query, values)
    self.connection.commit()
