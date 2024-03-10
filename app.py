from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# book_list = [
#   {
#     "id": 1,
#     "author": "J.K. Rowling",
#     "language": "English",
#     "title": "Harry Potter and the Philosopher's Stone"
#   },
#   {
#     "id": 2,
#     "author": "George Orwell",
#     "language": "English",
#     "title": "Nineteen Eighty-Four"
#   },
#   {
#     "id": 3,
#     "author": "Harper Lee",
#     "language": "English",
#     "title": "To Kill a Mockingbird"
#   },
#   {
#     "id": 4,
#     "author": "F. Scott Fitzgerald",
#     "language": "English",
#     "title": "The Great Gatsby"
#   },
#   {
#     "id": 5,
#     "author": "Gabriel García Márquez",
#     "language": "Spanish",
#     "title": "Cien años de soledad"
#   }
# ]

def db_connect():
    conn = None

    try:
        conn = sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn
        

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connect()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM book')

        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]

        return jsonify(books)

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']

        sql = """INSERT INTO book (author, language, title)
                VALUES (?, ?, ?)"""

        cursor.execute(sql, (new_author, new_lang, new_title))
        conn.commit()

        return f"Book with the id: {cursor.lastrowid} created successfully", 201


@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connect()
    cursor = conn.cursor()
    book = None

    if request.method == 'GET':
        sql = """SELECT * FROM book WHERE id=?"""
        cursor.execute(sql, (id,))

        row = cursor.fetchone()
        row_dict = {
            "id": row[0],
            "author": row[1],
            "language": row[2],
            "title": row[3]
        }

        if row is not None:
            return jsonify(row_dict), 200
        else:
            return "Book not found", 404
    
    if request.method == 'PUT':
        sql = """
            UPDATE book
            SET author=?,
                language=?,
                title=?
            WHERE id=?
        """

        author = request.form['author']
        language = request.form['language']
        title = request.form['title']

        conn.execute(sql, (author, language, title, id))
        conn.commit()

        updated_book = {
            "id": id,
            "author": author,
            "language": language,
            "title": title
        }

        return jsonify(updated_book), 200


    if request.method == 'DELETE':
        sql = """DELETE FROM book WHERE id=?"""
        cursor.execute(sql, (id,))
        conn.commit()

        return f"The book with the id: {id} has been deleted.", 200



if __name__ == '__main__':
    app.run()
