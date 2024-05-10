import datetime
from flask import render_template, request, make_response, jsonify
from app import app
import mysql.connector


db_user = 'uwi_user'
db_password = 'comp3161'
db_host = '127.0.0.1'
db_database = 'Project'

conn = mysql.connector.connect(user=db_user, password=db_password,
                               host=db_host, database=db_database)

@app.route('/registeruser', methods=['POST'])
def registerUser():
    # ○ A student/lecturer should be able to create an account.
    # ○ A user should be able to register with a userid and password
    # ○ A user can be an admin, lecturer or student

    cursor = conn.cursor()
    data = request.json
    fname = data['first_name']
    lname = data['last_name']
    user_role  = data['user_role']
    phoneNum = data['phone_number']
    address = data['address']
    uid = data['uid']
    password = data['password']
    cursor.execute("INSERT INTO Account (fname, lname, phoneNum, address, user_role, password) VALUES(%s, %s, %s, %s, %s, %s)",
                   (fname, lname, phoneNum, address, user_role, password))
    conn.commit()
    cursor.close()
    return make_response({'message':'User registered successfully'}, 201)

@app.route('/login', methods=['POST'])
def login():
    # ○ A student/lecturer should be able to login with credentials
    
    cursor = conn.cursor()
    data = request.json
    uid = data.get("uid")
    password = data.get("password")
    query = "SELECT * FROM Account WHERE uid = %s AND password = %s"
    cursor.execute(query, (uid, password))
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
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Course")
    return make_response({"success" : "Course(s) Retrieved"}, 201)

@app.route('/get_course/<userid>', methods=['GET'])
def getCourse(uid):
    # ○ Retrieve all the courses
    # ○ Retrieve courses for a particular student
    # ○ Retrieve courses taught by a particular lecturer
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Assigned WHERE uid == %s", uid)
    return make_response({"success" : "Course(s) Retrieved"}, 201)

@app.route('/registerforcourse')
def registerForCourse():
    # ○ Only one lecturer can be assigned to a course
    # ○ Students should be able to register for a course
    
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
        cursor.execute("INSERT INTO Assigned VALUES(%s, %s, %s, %s)", (cid, uid, semester, year))
        conn.commit()
    else:
        return make_response({'message': 'User not found'})


@app.route('/', methods=['GET'])
def hello_world():
    return "Hello👋, This is the API for our Virtual Learning Environment"


#get thread and first level replies
@app.route('/get_threads/<forum_id>', methods=['GET'])
def get_threads(forum_id):
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                       host=db_host,
                                       database=db_database)
        cursor = cnx.cursor()

        cursor.execute(f"SELECT tid, title, content, dateCreated FROM Thread WHERE parent = {forum_id}")
        threads = []

        for tid, title, content, dateCreated in cursor:
            thread = {
                'id': tid,
                'title': title,
                'content': content,
                'dateCreated': dateCreated,
                'replies': [] 
            }

            # Get replies for the current thread
            cursor.execute(f"SELECT reply_id, author, content, dateCreated FROM Reply WHERE parent = {tid}")
            for reply_id, reply_author, reply_content, reply_dateCreated in cursor:

                cursor.execute(f"SELECT fname, lname FROM Account WHERE uid = {reply_author}")
                fname, lname = cursor.fetchone()

                reply = {
                    'reply_id': reply_id,
                    'author': fname + " " + lname,
                    'content': reply_content,
                    'dateCreated': reply_dateCreated
                }
                thread['replies'].append(reply) 

            threads.append(thread)  

        cursor.close()
        cnx.close()

        return jsonify(threads), 200
    except Exception as e:
        return make_response({'error': str(e)}, 400)

#add thread to forum
@app.route('/add_thread', methods=['POST'])
def add_thread():
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                       host=db_host,
                                       database=db_database)
        cursor = cnx.cursor()

        # get JSON request
        content = request.json
        forum_id = content['forum_id']
        title = content['title']
        thread_content = content['content']
        date_created = content['createdAt']
        current_user = content['uid']

        cursor.execute(f"INSERT INTO Thread (parent, title, content, dateCreated) VALUES ({forum_id}, '{title}', '{thread_content}', '{date_created}')")

        tid = cursor.lastrowid
        cursor.execute(f"INSERT INTO ModifyThread (uid, tid) VALUES ({current_user}, {tid})")

        cnx.commit()
        cursor.close()
        cnx.close()
 
        return jsonify({"success": "Post added"}), 201
    except Exception as e:
        return make_response({'error': str(e)}, 400)

## -------------------
## REPLIES
## -------------------
#get replies for a reply
@app.route('/get_replies/<parent_id>', methods=['GET'])
def get_replies(parent_id):
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                       host=db_host,
                                       database=db_database)
        cursor = cnx.cursor()

        replies = []
        cursor.execute(f"SELECT reply_id, author, content, dateCreated FROM Reply WHERE parent = {parent_id}")
        
        for reply_id, author, content, dateCreated in cursor:

            cursor.execute(f"SELECT fname, lname FROM Account WHERE uid = {author}")
            fname, lname = cursor.fetchone()

            reply = {
                'reply_id': reply_id,
                'name': fname + " " + lname,
                'content': content,
                'dateCreated': dateCreated
            }
            replies.append(reply) 
        
        
        cursor.close()
        cnx.close()
 
        return jsonify(replies), 200
    except Exception as e:
        return make_response({'error': str(e)}, 400)

#add replies for a reply
@app.route('/add_reply', methods=['POST'])
def add_reply():
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                       host=db_host,
                                       database=db_database)
        cursor = cnx.cursor()

        content = request.json
        parent_id = content['forum_id']
        author = content['uid']
        reply_content = content['content']
        date_created = content['createdAt']

        cursor.execute(f"INSERT INTO Thread (parent, author, content, dateCreated) VALUES ({parent_id}, {author}, '{reply_content}', '{date_created}')")
        
        cnx.commit()
        cursor.close()
        cnx.close()
 
        return jsonify({"success": "Reply added"}), 201
    except Exception as e:
        return make_response({'error': str(e)}, 400)



## -------------------
## Course Content
## -------------------
#add section
@app.route('/add_section', methods=['POST'])
def add_section():
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                       host=db_host,
                                       database=db_database)
        cursor = cnx.cursor()

        content = request.json

        cid = content['cid']
        secName = content['section_name']
        lect_id = content['uid']

        cursor.execute(f"INSERT INTO Component (cid, compType) VALUES ('{cid}', 'Section')")

        comp_id = cursor.lastrowid
        
        cursor.execute(f"INSERT INTO Section VALUES ({comp_id}, '{cid}', '{secName}')")


        cursor.execute(f"INSERT INTO ModifySection VALUES ({lect_id}, {comp_id}, '{cid}')")

        
        cnx.commit()
        cursor.close()
        cnx.close()
 
        return jsonify({"success": "Section added"}), 201
    except Exception as e:
        return make_response({'error': str(e)}, 400)


#add section item
@app.route('/add_sectionItem', methods=['POST'])
def add_sectionItem():
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                       host=db_host,
                                       database=db_database)
        cursor = cnx.cursor()

        content = request.json
        lect_id = content['uid']
        parent_id = content['sec_id']
        parent_cid = content['cid']
        secItemName = content['item_name']
        itemType = content['item_type']
        contentPath = content['contentPath']

        cursor.execute(f"INSERT INTO SectionItems VALUES ({parent_id}, '{parent_cid}', '{secItemName}', '{itemType}', '{contentPath}')")
        item_id = cursor.lastrowid


        #add to modify items table
        cursor.execute(f"INSERT INTO ModifyItem VALUES ({item_id}, {lect_id})")

        cnx.commit()
        cursor.close()
        cnx.close()
 
        return jsonify({"success": "Item added"}), 201
    except Exception as e:
        return make_response({'error': str(e)}, 400)


#get course content
@app.route('/get_section/<cid>', methods=['GET'])
def get_course_sections(cid):
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                       host=db_host,
                                       database=db_database)
        cursor = cnx.cursor(dictionary=True) 
        
        cursor.execute(f"SELECT comp_id, secName FROM Section WHERE cid = '{cid}'")
        sections = cursor.fetchall()

        
        allContent = []

        for section in sections:
            comp_id = section['comp_id']
            section_name = section['secName']

            # get all section items for each section
            cursor.execute(f"SELECT item_id, item_name, item_type, contentPath FROM SectionItems WHERE parent_id = {comp_id} AND parent_cid = '{cid}'")
            section_items = cursor.fetchall()

            
            allContent.append({
                'comp_id': comp_id,
                'section_name': section_name,
                'section_items': section_items
            })

        cursor.close()
        cnx.close()

        return jsonify(allContent), 200
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
## -------------------
## Assignments
## -------------------
#submit assignment
@app.route('/course/<cid>/<assignId>/submit', methods=['POST'])
def submit_assignment(cid, assignId):
    try:
        
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                       host=db_host,
                                       database=db_database)
        cursor = cnx.cursor()

        
        content = request.json
        uid = content['uid'] 
        assignment_file = content.get('assignment_file')  
 
        cursor.execute(f"INSERT INTO Submit (comp_id, cid, uid, assignmentFile) VALUES ({assignId}, '{cid}', {uid}, '{assignment_file}')")
          
        cnx.commit()
        cursor.close()
        cnx.close()

       
        return jsonify({"success": "Assignment submitted successfully"}), 201
    except Exception as e:
        return make_response({'error': str(e)}, 400)

#give grade
@app.route('/course/<cid>/<assignId>/<uid>/grade', methods=['PUT'])
def grade_assignment(cid, assignId, uid):
    try:
       
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                       host=db_host,
                                       database=db_database)
        cursor = cnx.cursor()

        content = request.json
        grade = content['grade']

      
        cursor.execute(f"""
            UPDATE Submit
            SET grade = {grade}
            WHERE comp_id = {assignId} AND cid = '{cid}' AND uid = {uid}
        """)
        
        cnx.commit()
        cursor.close()
        cnx.close()

        return jsonify({"success": "Grade recorded successfully"}), 200

    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
#recalculate average
@app.route('/course/<cid>/<uid>/average', methods=['POST'])
def update_student_average(cid, uid):
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                       host=db_host,
                                       database=db_database)
        cursor = cnx.cursor(dictionary=True)
        
        cursor.execute(f"SELECT AVG(grade) AS average_grade FROM Submit WHERE cid = '{cid}' AND uid = {uid}GROUP BY uid")


        # get the avg as a dictionary
        result = cursor.fetchone()

        if result:
            average_grade = result['average_grade']
        else:
            return make_response({'error': 'There are no grades for the student for this course'}, 404)
        

        # Check if the student's grade already exists in the Enrol table
        cursor.execute(f"SELECT * FROM Enrol WHERE cid = '{cid}' AND uid = {uid}")
        existing_record = cursor.fetchone()

        if existing_record:
            cursor.execute(f"UPDATE Enrol SET grade = {average_grade} WHERE cid = '{cid}' AND uid = {uid}")
        else:
            cursor.execute(f"INSERT INTO Enrol (cid, uid, grade) VALUES ('{cid}', {uid}, {average_grade})")

        cnx.commit()
        cursor.close()
        cnx.close()

        return jsonify({"success": "Average recorded grade"}), 201
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
@app.route('/assignments/create', methods=['POST'])
def create_assignment():
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                      host=db_host, database=db_database)
        cursor = cnx.cursor()


        content = request.get_json
        cid = content['cid']
        due_date = content['due_date']
        assignment_name = content['assignment_name']
        description = content['description']
        instructions_file = content['instructions_file']
       
        cursor.execute(f"INSERT INTO Component (cid, compType) VALUES ('{cid}', 'Assignment')")
        comp_id = cursor.lastrowid

        cursor.execute(f"INSERT INTO Assignment (comp_id, cid, dueDate, assignmentName, description, instructionsFile) VALUES ({comp_id}, '{cid}', '{due_date}', '{assignment_name}', '{description}','{instructions_file}')")

        cnx.commit()
        cursor.close()
        cnx.close()

        return jsonify({"message": "Assignment created"}), 201
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)


## -------------------
## Reports
## -------------------
@app.route('/create_views', methods=['POST'])
def create_sql_views():
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                      host=db_host, database=db_database)
        cursor = cnx.cursor()

        # All courses that have 50 or more students
        cursor.execute("""
            CREATE OR REPLACE VIEW CoursesWith50 AS
            SELECT c.cid, c.cname, COUNT(e.uid) AS student_count
            FROM Course c
            JOIN Enrol e ON c.cid = e.cid
            GROUP BY c.cid
            HAVING COUNT(e.uid) >= 50;
        """)

        # All students that do 5 or more courses
        cursor.execute("""
            CREATE OR REPLACE VIEW StudentEnroll5 AS
            SELECT s.uid, a.fname, a.lname, COUNT(e.cid) AS course_count
            FROM Student s
            JOIN Enrol e ON s.uid = e.uid
            JOIN Account a ON s.uid = a.uid
            GROUP BY s.uid
            HAVING COUNT(e.cid) >= 5;
        """)

        #All lecturers that teach 3 or more courses
        cursor.execute("""
            CREATE VIEW LecTeaches3 AS
            SELECT l.uid, a.fname, a.lname, COUNT(cs.cid) AS course_count
            FROM Lecturer l
            JOIN Member m ON l.uid = m.uid
            JOIN Account a ON l.uid = a.uid
            JOIN Assigned cs ON l.uid = cs.uid
            GROUP BY l.uid
            HAVING COUNT(cs.cid) >= 3;
        """)

        #The 10 most enrolled courses
        cursor.execute("""
            CREATE VIEW MostEnrolledCourses AS
            SELECT c.cid, c.cname, COUNT(e.uid) AS student_count
            FROM Course c
            JOIN Enrol e ON c.cid = e.cid
            GROUP BY c.cid, c.cname
            ORDER BY student_count DESC
            LIMIT 10;              
        """)

        #The top 10 students with the highest overall averages
        cursor.execute("""
            CREATE VIEW StudentsHighestAverage AS
            SELECT s.uid, a.fname, a.lname, AVG(su.grade) AS average_grade
            FROM Student s
            JOIN Account a ON s.uid = a.uid
            LEFT JOIN Submit su ON s.uid = su.uid
            GROUP BY s.uid, a.fname, a.lname
            ORDER BY average_grade DESC
            LIMIT 10;    
        """)
 
    
        cnx.commit()
        cursor.close()
        cnx.close()

        return jsonify({"message": "Views created"}), 201
    except Exception as e:
        return make_response({"error": str(e)}, 400)


@app.route('/report', methods=['GET'])
def get_report():
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_database)
        cursor = cnx.cursor()

        views = [
            "CoursesWith50",
            "StudentEnroll5",
            "LecTeaches3",
            "MostEnrolledCourses",
            "StudentsHighestAverage"
        ]
        
        results = {}

        for view_name in views:
            cursor.execute(f"SELECT * FROM {view_name};")
            view_data = cursor.fetchall()

            results[view_name] = view_data

        cursor.close()
        cnx.close()

        return jsonify(results), 200
    except Exception as e:
        return make_response({"error": str(e)}, 400)
