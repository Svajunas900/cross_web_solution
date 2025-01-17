from postgresConnection import PostgresConnection
from sqliteConnection import SqliteConnection


class DBAdapter:
  def fetch_data(self):
    return
  
  def save_data(self, data):
    return
  

class DatabaseAdapter(DBAdapter):
  def __init__(self, db_type):
    if db_type == "postgresql":
      self.db = PostgresConnection()
    elif db_type == "sqlite":
      self.db = SqliteConnection()
    else:
      raise ValueError("Unsupported DB type")
  
  def fetch_data(self, query):
    return self.db.fetch_data(query)
  
  def save_data(self, query):
    self.db.save_data(query)


def transfer_data():
  
  postgres_adapter = DatabaseAdapter('postgresql')
  
  postgres_query = ""
  data = postgres_adapter.fetch_data(postgres_query)


  sqlite_adapter = DatabaseAdapter('sqlite')
  sqlite_query = ""
  
  sqlite_adapter.save_data(sqlite_query)