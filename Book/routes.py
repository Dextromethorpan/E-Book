"""
User API Endpoints:
/api/book/all              - GET
/api/book/create           - POST
/api/bok/<book-title>      - POST

"""


from flask import Blueprint, request, jsonify
from models import Book, db
book_blueprint = Blueprint('book_api_routes', __name__, url_prefix='/api/book')


@book_blueprint.route('/all', methods=['GET'])
def get_all_books():
    all_books = Book.query.all()
    result = [book.serialize() for book in all_books]
    response = {"result":result}
    return jsonify(response)

@book_blueprint.route('/create', methods=['POST'])
def create_books():
    try:
        # Create a new Book instance and map form data to the model fields
        book = Book()
        book.isbn=request.json.get('isbn')  # Expecting 'isbn' from the form data
        book.title=request.json.get('title')  # Expecting 'title' from the form data
        book.author=request.json.get('author')  # Optional field 'author'
        book.year_of_publication=request.json.get('year_of_publication')  # Optional field
        book.publisher=request.json.get('publisher')  # Optional field
        book.image_url_s=request.json.get('image_url_s')  # Optional field
        book.image_url_m=request.json.get('image_url_m')  # Optional field
        book.image_url_l=request.json.get('image_url_l')  # Optional field

        print(book.isbn)
        print(book.author)
        print(book.title)

        # Add the book to the session and commit the transaction
        db.session.add(book)
        db.session.commit()

        # Return a success response with the serialized book data
        response = {'message': 'Book Created', 'result': book.serialize()}
    except Exception as e:
        print(str(e))  # Log the error
        response = {'message': 'Book creation failed', 'error': str(e)}  # Include error message in the response

    return jsonify(response)


@book_blueprint.route('/<title>', methods=['GET'])
def book_details(title):
    book = Book.query.filter_by(title=title).first()
    if book:
        response = {"result": book.serialize()}
    else:
        response = {"message": "No book found"}

    return jsonify(response)
