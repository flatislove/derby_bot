import psycopg2
from src.config import host,user,password,db_name

def get_from_database(text):
  try:
    connection=psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name)
    connection.autocommit=True
    with connection.cursor() as cursor:
      cursor.execute(text)
      return cursor.fetchall()
  except Exception as ex:
    print("[INFO] Error while working with Postgres",ex)
    return -1
  finally:
    if connection:
      connection.close()

def add_to_database(add):
  connection=None
  try:
    connection=psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name)
    connection.autocommit=True
    with connection.cursor() as cursor:
        cursor.execute(add)
  except Exception as ex:
    print("[INFO] Error while working with Postgres",ex)
    return -1
  finally:
    if connection:
      connection.close()

def add_tables():
    sql=        """
        CREATE TABLE IF NOT EXISTS "Team"(
            id serial PRIMARY KEY,
            name varchar(50) NOT NULL
            );

        CREATE TABLE IF NOT EXISTS "Position"(
            id serial PRIMARY KEY,
            name varchar(4) NOT NULL
            );

        CREATE TABLE IF NOT EXISTS "Player"(
            id serial PRIMARY KEY,
            firstname varchar(50) NOT NULL,
            lastname varchar(50) NOT NULL,
            team_id integer,
            number varchar(15),
            position_id integer,
            FOREIGN KEY (team_id) REFERENCES "Team" (id)
            ON DELETE CASCADE,
            FOREIGN KEY (position_id) REFERENCES "Position" (id)
            ON DELETE CASCADE
            );"""
    add_to_database(sql)