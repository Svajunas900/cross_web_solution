import psycopg2
import os 
from dotenv import load_dotenv

load_dotenv()


POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


class PostgresConnection:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls, *args, **kwargs)
      cls._instance.connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT)
      cls._instance.cursor = cls._instance.connection.cursor()
      return cls._instance
  
  def fetch_data(self, query):
    self.cursor.execute(query)
    return self.cursor.fetchall()

  def save_data(self, query, values):
    self.cursor.executemany(query, values)
    self.connection.commit()


# conn = PostgresConnection()

# print(conn.fetch_data("SELECT * FROM app1_userprofile"))
