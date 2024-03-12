from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def db_connect():
    conn = None

    try:
        conn = pymysql.connect(
            host='sql6.freesqldatabase.com',
            database='sql6690160',
            user='sql6690160',
            password='jWtPvCpvdH',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(e)
    return conn
        

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connect()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM book')

        books = cursor.fetchall()

        return jsonify(books)

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']

        sql = """
            INSERT INTO book (author, language, title)
            VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (new_author, new_lang, new_title))
        conn.commit()

        return f"Book with the id: {cursor.lastrowid} created successfully", 201


@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connect()
    cursor = conn.cursor()
    book = None

    if request.method == 'GET':
        sql = """SELECT * FROM book WHERE id=%s"""
        cursor.execute(sql, (id,))

        row = cursor.fetchone()

        if row is not None:
            return jsonify(row), 200
        else:
            return "Book not found", 404
    
    if request.method == 'PUT':
        sql = """
            UPDATE book
            SET author=%s,
                language=%s,
                title=%s
            WHERE id=%s
        """

        author = request.form['author']
        language = request.form['language']
        title = request.form['title']

        cursor.execute(sql, (author, language, title, id))
        conn.commit()

        updated_book = {
            "id": id,
            "author": author,
            "language": language,
            "title": title
        }

        return jsonify(updated_book), 200


    if request.method == 'DELETE':
        sql = """DELETE FROM book WHERE id=%s"""
        cursor.execute(sql, (id,))
        conn.commit()

        return f"The book with the id: {id} has been deleted.", 200



if __name__ == '__main__':
    app.run()
