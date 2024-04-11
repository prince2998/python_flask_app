from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'prince'
app.config['MYSQL_DB'] = 'students'
mysql = MySQL(app)

# Function to create database and student table if they don't exist
# Serve static files (HTML and CSS)
@app.route('/')
def create_database_and_table():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS students")
        cur.execute("USE students")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS student (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT
            )
        """)
        mysql.connection.commit()
        cur.close()

# Serve static files (HTML and CSS)
#@app.route('/')
def index():
    return render_template('index.html')

# API endpoints for CRUD operations
@app.route('/students', methods=['POST'])
def add_student():
    data = request.form
    name = data['name']
    age = data['age']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO student (name, age) VALUES (%s, %s)", (name, age))
    mysql.connection.commit()
    cur.close()
    return render_template('success.html')

# API endpoints
@app.route('/students', methods=['GET'])
def get_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    data = cur.fetchall()
    cur.close()
    return render_template('students.html', students=data)

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    data = cur.fetchone()
    cur.close()
    return render_template('student.html', student=data)

# Add other CRUD endpoints (POST, PUT, DELETE) as needed
@app.route('/update/<int:student_id>', methods=['PUT', 'POST'])
def update_student(student_id):
    if request.method in ['POST','PUT']:
        data = request.form
        name = data['name']
        age = data['age']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE student SET name = %s, age = %s WHERE id = %s", (name, age, student_id))
        mysql.connection.commit()
        cur.close()
        return render_template('update.html', student=data)
    else:
        # Handle other HTTP methods (e.g., GET, DELETE)
        return jsonify({"error": "Method Not Allowed"}), 405

@app.route('/delete/<int:student_id>', methods=['DELETE','POST'])
def delete_student(student_id):
    if request.method in ['DELETE','POST']:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM student WHERE id = %s", (student_id,))
        mysql.connection.commit()
        cur.close()

        return render_template('delete.html', student=data)
    else:
        # Handle other HTTP methods (e.g., GET, DELETE)
        return jsonify({"error": "Method Not Allowed"}), 405

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
