from flask import Flask, request, jsonify

app = Flask(__name__)

book_list = [
  {
    "id": 1,
    "author": "J.K. Rowling",
    "language": "English",
    "title": "Harry Potter and the Philosopher's Stone"
  },
  {
    "id": 2,
    "author": "George Orwell",
    "language": "English",
    "title": "Nineteen Eighty-Four"
  },
  {
    "id": 3,
    "author": "Harper Lee",
    "language": "English",
    "title": "To Kill a Mockingbird"
  },
  {
    "id": 4,
    "author": "F. Scott Fitzgerald",
    "language": "English",
    "title": "The Great Gatsby"
  },
  {
    "id": 5,
    "author": "Gabriel García Márquez",
    "language": "Spanish",
    "title": "Cien años de soledad"
  }
]

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        if len(book_list) > 0:
            return jsonify(book_list)
        else:
            return 'Nothing found', 404

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        new_id = book_list[-1]['id'] + 1

        new_obj = {
            'id': new_id,
            'author': new_author,
            'language': new_lang,
            'title': new_title
        }

        book_list.append(new_obj)
        return jsonify(book_list), 201


@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in book_list:
            if book['id'] == id:
                return jsonify(book)
            pass
    
    if request.method == 'PUT':
        for book in book_list:
            if book['id'] == id:
                book['author'] = request.form['author']
                book['language'] = request.form['language']
                book['title'] = request.form['title']

                updated_book = {
                    'id': id,
                    'author': book['author'],
                    'language': book['language'],
                    'title': book['title']
                }

                return jsonify(updated_book)

    if request.method == 'DELETE':
        for index, book in enumerate(book_list):
            if book['id'] == id:
                book_list.pop(index)
                return jsonify(book_list), 200

if __name__ == '__main__':
    app.run()
