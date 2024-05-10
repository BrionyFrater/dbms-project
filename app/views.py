import datetime
from flask import render_template, request, make_response
from app import app
import mysql.connector

db_config = {
    'user': 'uwi_user',
    'password': 'uwi876',
    'host': '127.0.0.1',
    'database': 'Project'
}

conn = mysql.connector.connect(**db_config)

@app.route('/registeruser', methods=['POST'])
def registerUser():
    # ○ A student/lecturer should be able to create an account.
    # ○ A user should be able to register with a userid and password
    # ○ A user can be an admin, lecturer or student
    # conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
    #                                database='uwi')
    cursor = conn.cursor()
    data = request.json
    fname = data['first_name']
    lname = data['last_name']
    user_role  = data['user_role']
    phoneNum = data['phone_number']
    address = data['address']
    uid = data['uid']
    password = data['password']
    cursor.execute(f"INSERT INTO Account VALUES('{uid}', '{fname}', '{lname}',  
                   '{phoneNum}', '{address}', '{user_role}', 1, '{password}')")
    conn.commit()
    cursor.close()
    return make_response({'message':'User registered successfully'}, 201)

@app.route('/login', methods=['POST'])
def login():
    # ○ A student/lecturer should be able to login with credentials
    # conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
    #                                database='uwi')
    cursor = conn.cursor()
    uid = request.json.get("uid")
    password = request.json.get("password")
    # user_role = request.json.get("user_role")
    query = "SELECT * FROM Account WHERE uid = %s AND password = %s"
    cursor.execute(query, uid, password)
    # if username == "" and password == "" and user_role in Account:
    #     if user_role == "Student":
    #         pass
    #     elif user_role == "Lecturer":
    #         pass
    #     else:
    #         pass
    user = cursor.fetchone()
    cursor.close()
    if user:
        return make_response({'message': 'Logged in successfully'}, 200)
    else:
        return make_response({'message': 'Invalid username or password'}, 400)

@app.route('/createcourse', methods=['POST'])
def createCourse(adminid):
    # ○ An admin should be able to create a course
    # ○ Only admins should be able to create a course
    # conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
    #                                database='uwi')
    cursor = conn.cursor()
    content = request.json
    if adminid == content['id']:
        id = content['id']
    cid = content['last_name']
    dateCreated = datetime
    cname = content['name']
    cursor.execute(f"INSERT INTO CreateCrse VALUES('{id}','{cid}','{dateCreated}')")
    cursor.execute(f"INSERT INTO Course VALUES('{cid}','{cname}','{dateCreated}')")
    conn.commit()
    cursor.close()
    conn.close()
    return make_response({"success" : "Course Created"}, 201)

@app.route('/get_courses', methods=['GET'])
def getCourses():
    # ○ Retrieve all the courses
    # ○ Retrieve courses for a particular student
    # ○ Retrieve courses taught by a particular lecturer
    # conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
    #                                database='uwi')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Course")
    return make_response({"success" : "Course(s) Retrieved"}, 201)

@app.route('/get_course/userid', methods=['GET'])
def getCourse(uid):
    # ○ Retrieve all the courses
    # ○ Retrieve courses for a particular student
    # ○ Retrieve courses taught by a particular lecturer
    # conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
    #                                database='uwi')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Assigned WHERE '{uid}' == Assigned.uid")
    return make_response({"success" : "Course(s) Retrieved"}, 201)

@app.route('/registerforcourse')
def registerForCourse():
    # ○ Only one lecturer can be assigned to a course
    # ○ Students should be able to register for a course
    # conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
    #                                database='uwi')
    cursor = conn.cursor()
    data = request.json
    uid = data['uid']
    cid = data['cid']
    semester = data['semester']
    year = data['year']
    user_role = data['user_role']

    if user_role == "student":
        query = "SELECT * FROM Student WHERE uid == %s"
    elif user_role == "lecturer":
        query == "SELECT * FROM Lecturer WHERE uid == %s"
    else:
        return make_response({'message': 'Invalid user role'})
    cursor.execute(query, uid)
    user = cursor.fetchone()

    if user:
        cursor.execute(f"INSERT INTO Assigned VALUES('{cid}', '{uid}', '{semester}', '{year}')")
        conn.commit()
    else:
        return make_response({'message': 'User not found'})