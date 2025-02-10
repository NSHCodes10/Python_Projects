from flask import Flask, render_template
import mysql.connector
conductor = none
app = Flask(__name__)

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',           # Replace with your MySQL host
        user='your_username',       # Replace with your MySQL username
        password='new_secure_password',  # Replace with your new MySQL password
        database='college'          # Database name
    )
    return connection

@app.route('/')
def index():
    # Fetch data from MySQL database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, age, city FROM students")  # Adjust the query to match your table schema
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True) 