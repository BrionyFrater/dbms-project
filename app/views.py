from flask import render_template, request, make_response
from app import app
import mysql.connector

#Return members of a course
@app.route('/membersofcourse/<courseid>',methods=['GET'])
def getMembersOfACourse(courseid):
    try:
        conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
                                   database='uwi')
        cursor = conn.cursor()
        query = """
        SELECT Account.uid, Account.fname, Account.lname, Account.phoneNum, Account.user_role
        FROM Account
        JOIN Member ON Account.uid = Member.uid
        JOIN Assigned ON Member.uid = Assigned.uid
        WHERE Assigned.cid = '{courseid}';"""
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            getMembersOfACourse= {
                'ID': row[0],
                'Firstname': row[1],
                'Lastname': row[2],
                'PhoneNumber': row[3],
                'Role': row[4]
            }
            result.append(getMembersOfACourse)

        # Close cursor and connection
        cursor.close()

        return make_response(result, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


#retrieve all calendar events
@app.route('/calendarevents/<courseid>',methods=['GET'])
def getCalendarEvents(courseid):
    try:
        conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
                                   database='uwi')
        cursor = conn.cursor()
        query = """
        SELECT *
        FROM Event
        WHERE cid ='{courseid}';"""
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            getCalendarEvents= {
                'courseID': row[0],
                'EventID': row[1],
                'name': row[2],
                'description': row[3],
                'datecreated': row[4],
                'duedate':row[5]
            }
            result.append(getCalendarEvents)

        # Close cursor and connection
        cursor.close()

        return make_response(result, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
#retrieve calendar events for particular date and student
@app.route('/calendarevent/<date>/<student_id>',methods=['POST'])
def getCalendarEvent(date,student_id):
    try:
        conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
                                   database='uwi')
        cursor = conn.cursor()
        data = request.json
        query = """
        SELECT e.name, e.description, e.dueDate
FROM Event e
JOIN Component c ON e.comp_id = c.comp_id AND e.cid = c.cid
JOIN Course cr ON c.cid = cr.cid
JOIN Enrol en ON cr.cid = en.cid
JOIN Student s ON en.uid = s.uid
WHERE s.uid = {student_id}
AND e.dueDate = '{date}';"""
        cursor.execute(query,(student_id,date))
        result = []
        for row in cursor.fetchall():
            getCalendarEvent= {
                'courseID': row[0],
                'componentID': row[1],
                'name': row[2],
                'description': row[3],
                'datecreated': row[4],
                'duedate':row[5]
            }
            result.append(getCalendarEvent)

        # Close cursor and connection
        cursor.close()

        return make_response(result, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

#create calendar events
@app.route('/addcalendarevents/<course_id>', methods=['POST'])
def addcalendarevents(course_id):
    try:
        conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
                                   database='uwi')
        cursor = conn.cursor()
        content = request.json
        course_id =content ['course_id']
        component_id = content ['component_id']
        event_name= content ['Name']
        event_description = content ['Description']
        event_date_created = content ['Date created']
        event_due_date = content ['Due Date']
        
        cursor.execute(f"INSERT INTO Event VALUES ('{course_id}', {component_id}, '{event_name}', '{event_description}', '{event_date_created}', '{event_due_date}')")
        cursor.close()
        return make_response({"success" : "Event added"}, 201)
    except Exception as e:
        print(e)
        return make_response({'error': 'An error has occured'}, 400)
    
#retreive forums for a course
@app.route('/forum/<courseid>',methods=['GET'])
def getforum(courseid):
    try:
        conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
                                   database='uwi')
        cursor = conn.cursor()
        query = """
        SELECT f.name, f.dateCreated
FROM Forum f
JOIN Component c ON f.comp_id = c.comp_id AND f.cid = c.cid
WHERE c.cid = '{courseid}';"""
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            getforum= {
                'courseID': row[0],
                'componentID': row[1],
                'name': row[2],
                'ddatecreated': row[3]
            }
            result.append(getforum)

        # Close cursor and connection
        cursor.close()

        return make_response(result, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
#create forum for a course
@app.route('/addforum/<course_id>', methods=['POST'])
def addforum():
    try:
        conn = mysql.connector.connect(user='uwi_user', password='uwi876', host='127.0.0.1',
                                   database='uwi')
        cursor = conn.cursor()
        content = request.json
        course_id =content ['course_id']
        component_id = content ['component_id']
        name= content ['Name']
        date_created = content ['Date created']
       
        
        cursor.execute(f"INSERT INTO Forum VALUES ('{course_id}', {component_id}, '{name}','{date_created}')")
        cursor.close()
        return make_response({"success" : "Event added"}, 201)
    except Exception as e:
        print(e)
        return make_response({'error': 'An error has occured'}, 400)
