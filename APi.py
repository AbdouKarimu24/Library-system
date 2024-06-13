from flask import Flask, request, jsonify
import MySQLdb

app = Flask(__name__)

# Database connection configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'toor'  # Updated password
DB_NAME = 'library'

# Helper functions for database operations
def connect_to_database():
    return MySQLdb.connect(host='localhost', user='root', password='toor', db='library')

def execute_query(query, params=None):
    connection = connect_to_database()
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    connection.commit()
    result = cursor.fetchall()
    connection.close()
    return result

# API Key verification decorator
def require_api_key(func):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key == '12345':
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'Invalid API key'}), 401
    decorated_function.__name__ = func.__name__  # Set the name of the decorated function
    return decorated_function

# API Endpoints
@app.route('/login', methods=['POST'])
@require_api_key
def login():
    data = request.json
    username = data['username']
    password = data['password']
    query = "SELECT * FROM users WHERE user_name = %s AND user_password = %s"
    result = execute_query(query, (username, password))
    if result:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/books', methods=['GET', 'POST'])
@require_api_key
def manage_books():
    if request.method == 'GET':
        # Retrieve all books from the database
        query = "SELECT * FROM book"
        books = execute_query(query)
        return jsonify({'books': books}), 200
    elif request.method == 'POST':
        # Add a new book to the database
        data = request.json
        book_title = data['book_title']
        # Extract other book details from the request
        # Perform insertion into the database
        query = "INSERT INTO book (book_title) VALUES (%s)"
        execute_query(query, (book_title,))
        return jsonify({'message': 'Book added successfully'}), 201

# Additional endpoints can be created for managing clients, users, and other operations

if __name__ == '__main__':
    app.run(debug=True)