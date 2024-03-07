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
            'Nothing found', 404

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


if __name__ == '__main__':
    app.run()
