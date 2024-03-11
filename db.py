import pymysql.cursors

conn = pymysql.connect(
  host='sql6.freesqldatabase.com',
  database='sql6690160',
  user='sql6690160',
	password='jWtPvCpvdH',
  charset='utf8mb4',
  cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

sql_query = """
  CREATE TABLE book (
    id integer PRIMARY KEY AUTO_INCREMENT,
    author text NOT NULL,
    language text NOT NULL,
    title text NOT NULL
  )
"""

cursor.execute(sql_query)
conn.close()
