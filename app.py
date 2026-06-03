from flask import Flask, render_template, request, redirect,session
from db_config import get_db_connection

#create a flask application 
app = Flask(__name__)

app.secret_key = 'secrete123'

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """SELECT * 
        FROM users 
        WHERE username = %s 
        AND password = %s
        """
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            session['user_id'] = user['user_id']
            session['full_name'] = user['full_name']
            return redirect('/')
        else:
            return render_template(
                'login.html', 
                error='Invalid username or password'
            )
    return render_template(
        'login.html',
        error=None
        )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/') 
def home():
    
    if 'user_id' not in session:
        return redirect('/login')

    connection = get_db_connection() 


    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM student")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_attendance = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        'index.html',
        total_students=total_students,
        total_attendance=total_attendance,
        total_tasks=total_tasks
        )
@app.route('/student')
def student_list():
    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    querry = 'SELECT * FROM student'

    cursor.execute(querry)

    student_list = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('student.html', students=student_list)
#Add student page 
@app.route('/add_student/', methods=['GET','POST'])
def add_student():

    #check from submission 
    if request.method == 'POST':

        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        mobile_number = request.form['mobile_number']
        course_name = request.form['course_name']
        email = request.form['email']
      
        # Create database connection 
        connection = get_db_connection()

        #Create cusor object 
        cursor = connection.cursor()

        #sql Instert querry 
        querry = 'INSERT INTO student (first_name, last_name, gender, mobile_number,course_name, email) VALUES (%s, %s, %s, %s, %s, %s)'

        #Execute querry 
        cursor.execute(querry, (first_name, last_name, gender, mobile_number, course_name, email))

        #save changes 
        connection.commit()

        #Close database connection
        cursor.close()
        connection.close()

        return 'Student added successfully!'
    
    return render_template('add_student.html')

@app.route('/edit_student/<int:student_id>')
def edit_student(student_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    querry = 'SELECT * FROM student WHERE student_id = %s'
    cursor.execute(querry, (student_id,))

    student = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template('edit_student.html', student=student)

@app.route ('/update_student/<int:student_id>', methods=['POST'])
def update_student(student_id):

    # Get form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    connection = get_db_connection()
    cursor = connection.cursor()
    querry = 'UPDATE student SET first_name = %s, last_name = %s WHERE student_id = %s'
    cursor.execute(querry, (first_name, last_name, student_id))
    connection.commit()

    cursor.close()
    connection.close()
 
    return redirect('/student')

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):

    connection = get_db_connection()
    cursor = connection.cursor()
    querry = 'DELETE FROM student WHERE student_id = %s'
    cursor.execute(querry, (student_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/student')

@app.route('/attendance')
def attendance():
    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    querry = 'SELECT * FROM student'

    cursor.execute(querry)

    student_list = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('attendance.html', students=student_list)
@app.route('/save_attendance', methods=['POST'])
def save_attendance():

    student_id = request.form['student_id']
    attendance_status = request.form['attendance_status']

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO attendance
    (student_id, attendance_date, attendance_status)
    VALUES (%s, CURDATE(), %s)
    """

    cursor.execute(query, (student_id, attendance_status))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/attendance')

@app.route('/attendance_report')
def attendance_report():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    querry = '''
    SELECT 
       attendance.attendance_id,
       attendance.attendance_date,
       attendance.attendance_status,

        student.first_name,
        student.last_name,
        student.course_name

    FROM attendance
    
    INNER JOIN student 
            ON attendance.student_id = student.student_id

    ORDER BY attendance.attendance_date DESC
    '''

    cursor.execute(querry)

    attendance_records = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('attendance_report.html', attendance_records=attendance_records)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():


    if request.method == 'POST':

        task_name = request.form['task_name']
        task_description = request.form['task_description']
        maximum_marks = request.form['maximum_marks']

        connection = get_db_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO tasks
        (
        task_name, 
        task_description, 
        maximum_marks
        ) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(
            query,
            (
            task_name, 
            task_description, 
            maximum_marks
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect('/tasks')
    return render_template('add_task.html')

@app.route('/tasks')
def task_list():
    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    querry = """
    SELECT * 
    FROM tasks
    order by task_id DESC
    """

    cursor.execute(querry)

    task_list = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template(
        'tasks.html', 
        tasks=task_list
        )
@app.route('/assign_task', methods=['GET','POST'])
def assign_task():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':

        student_id = request.form['student_id']
        task_id = request.form['task_id']
      
        obtained_marks = 0
        query = """
        INSERT INTO student_tasks
        (
            student_id, 
            task_id, 
            obtained_marks,
            submission_date
        ) 
        VALUES (%s, %s, %s , CURDATE())
        """
        cursor.execute(
            query,
            (
                student_id, 
                task_id, 
                obtained_marks
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect('/student_tasks')

    cursor.execute('SELECT * FROM student')
    students = cursor.fetchall()

    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        'assign_task.html', 
        students=students, 
        tasks=tasks
    )

@app.route('/student_tasks')
def student_tasks():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    querry = """
    SELECT 
        student_tasks.student_task_id,
        student_tasks.obtained_marks,
        student_tasks.submission_date,

        student.first_name,
        student.last_name,

        tasks.task_name

    FROM student_tasks
    
    INNER JOIN student 
            ON student_tasks.student_id = student.student_id

    INNER JOIN tasks
            ON student_tasks.task_id = tasks.task_id

    ORDER BY student_tasks.student_task_id DESC
    """

    cursor.execute(querry)

    student_tasks_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('student_tasks.html', student_tasks=student_tasks_list)


# #Edit student page
# @app.route('/edit_student.html/<int:student_id>', methods=['GET', 'POST']) 
# def edit_student(student_id):

#     #Create database connection
#     connection = get_db_connection()

#     #Create cursor object
#     cursor = connection.cursor(dictionary=True)

#     #Check from submission
#     if request.method == 'POST':

#         # Get form data
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']  
#         gerder = request.form['gender']
#         mobile_number = request.form['mobile_number']
#         course_name = request.form['course_name']
#         email = request.form['email']

#         #SQL Update querry
#         querry = """
#         UPDATE student
#         SET
#             first_name = %s,
#             last_name = %s
#             gender = %s,
#             mobile_number = %s,
#             course_name = %s,
#             email = %s
#         WHERE student_id = %s
#         """
#         #Execute querry
#         cursor.execute(
#             querry,
#             (  first_name, 
#                last_name, 
#                gender, 
#                mobile_number, 
#                course_name, 
#                email, 
#                student_id
#             )
#         )

#         #save changes
#         connection.commit()

#         #Close connection
#         cursor.close()
#         connection.close()

#         return 'Student updated successfully!'
    
#     return render_template('edit_student.html')

# Student performance report
@app.route('/performance_report')
def performance_report():

    # Create database connection
    connection = get_db_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # SQL query with GROUP BY and aggregate functions
    query = """
        SELECT

            students.student_id,
            students.first_name,
            students.last_name,
            students.course_name,

            COUNT(student_tasks.student_task_id)
                AS total_tasks,

            SUM(student_tasks.obtained_marks)
                AS total_marks,

            AVG(student_tasks.obtained_marks)
                AS average_marks,

            SUM(
                CASE
                    WHEN student_tasks.submission_status = 'Submitted'
                    THEN 1
                    ELSE 0
                END
            ) AS submitted_tasks

        FROM students

        LEFT JOIN student_tasks
            ON students.student_id = student_tasks.student_id

        GROUP BY
            students.student_id,
            students.first_name,
            students.last_name,
            students.course_name

        ORDER BY total_marks DESC
    """

    # Execute query
    cursor.execute(query)

    # Fetch report data
    performance_records = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Load report page
    return render_template(
        'performance_report.html',
        performance_records=performance_records
    )

# Attendance summary report
@app.route('/attendance_summary')
def attendance_summary():

    # Create database connection
    connection = get_db_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # SQL summary query
    query = """
        SELECT

            attendance_date,

            COUNT(attendance_id)
                AS total_records,

            SUM(
                CASE
                    WHEN attendance_status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ) AS total_present,

            SUM(
                CASE
                    WHEN attendance_status = 'Absent'
                    THEN 1
                    ELSE 0
                END
            ) AS total_absent,

            SUM(
                CASE
                    WHEN attendance_status = 'Leave'
                    THEN 1
                    ELSE 0
                END
            ) AS total_leave

        FROM attendance

        GROUP BY attendance_date

        ORDER BY attendance_date DESC
    """

    # Execute query
    cursor.execute(query)

    # Fetch records
    attendance_summary_records = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Load page
    return render_template(
        'attendance_summary.html',
        attendance_summary_records=attendance_summary_records
    )

if __name__ == '__main__':
    app.run(debug=True)
    