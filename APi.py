from flask import Flask, request, jsonify
import MySQLdb

app = Flask(__name__)

# Database connection configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'library'

# Helper functions for database operations
def connect_to_database():
    return MySQLdb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)

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

# API Endpoints
@app.route('/login', methods=['POST'])
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