from postgresConnection import PostgresConnection
from sqliteConnection import SqliteConnection


class DBAdapter:
  def fetch_data(self, query):
    return
  
  def save_data(self, query, data):
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
  
  def save_data(self, query, data):
    self.db.save_data(query, data)


def transfer_data(table):
  
  postgres_adapter = DatabaseAdapter('postgresql')

  postgres_query = f"SELECT * FROM {table}"
  data = postgres_adapter.fetch_data(postgres_query)

  length = ""
  if data:
    length = len(data[0])
  else:
    length = 0

  sqlite_adapter = DatabaseAdapter('sqlite')
  sqlite_query = f"INSERT INTO {table} VALUES({'?, '* (length-1) + '?'})"
  sqlite_adapter.save_data(sqlite_query, data)

# transfer_data('app1_userprofile')
# transfer_data('app1_age')
# transfer_data('app1_belt')
# transfer_data('app1_brackets')
# transfer_data('app1_city')
# transfer_data('app1_competition')
# transfer_data('app1_competitorlevel')
# transfer_data('app1_weight')
# transfer_data('auth_group')

def select_data(table):
  sqlite_adapter = DatabaseAdapter("sqlite")
  query = f"SELECT * FROM {table}"
  print(sqlite_adapter.fetch_data(query))

# select_data("auth_user")