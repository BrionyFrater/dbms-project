from flask import render_template, request, make_response, jsonify
from app import app
import mysql.connector

db_user = 'project_user'
db_password = '123'
loggedInUser = {
    'uid' : 618,
    'name': 'Greg Han',
    'role': 'Lecturer'
}
@app.route('/', methods=['GET'])
def hello_world():
    return "Hello👋, This is the API for our Virtual Learning Environment"

# @app.route('/get_threads/<forum_id>', methods=['GET'])
# def get_threads(forum_id):
#     try:
#         cnx = mysql.connector.connect(user=db_user, password=db_password,
#                                 host='127.0.0.1',
#                                 database='Project')
#         cursor = cnx.cursor()
#         cursor.execute(f"SELECT tid, title, content, dateCreated from Thread WHERE parent={forum_id}")
#         threads = []
#         for tid, title, content, dateCreated in cursor:
#             thread = {}
#             thread['id'] = tid
#             thread['title'] = title
#             thread['content'] = content
#             thread['dateCreated'] = dateCreated

#             cursor.execute(f"SELECT reply_id, content, dateCreated from Reply WHERE parent={tid}")

#             threads.append(thread)
#         cursor.close()
#         cnx.close()
#         return make_response(threads, 200)
#     except Exception as e:
#         return make_response({'error': str(e)}, 400)

#get thread and first level replies
@app.route('/get_threads/<forum_id>', methods=['GET'])
def get_threads(forum_id):
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                       host='127.0.0.1',
                                       database='Project')
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
            cursor.execute(f"SELECT reply_id, content, dateCreated FROM Reply WHERE parent = {tid}")
            for reply_id, reply_content, reply_dateCreated in cursor:
                reply = {
                    'reply_id': reply_id,
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
                                       host='127.0.0.1',
                                       database='Project')
        cursor = cnx.cursor()

        # get JSON request
        content = request.json
        forum_id = content['forum_id']
        title = content['title']
        thread_content = content['content']
        date_created = content['createdAt']

        cursor.execute(f"INSERT INTO Thread (parent, title, content, dateCreated) VALUES ({forum_id}, {title}, {thread_content}, {date_created})")

        tid = cursor.lastrowid
        cursor.execute(f"INSERT INTO ModifyThread (uid, tid) VALUES ({loggedInUser['uid']}, {tid})")

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
                                       host='127.0.0.1',
                                       database='Project')
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
                                       host='127.0.0.1',
                                       database='Project')
        cursor = cnx.cursor()

        content = request.json
        parent_id = content['forum_id']
        author = content['uid']
        reply_content = content['content']
        date_created = content['createdAt']

        cursor.execute(f"INSERT INTO Thread (parent, author, content, dateCreated) VALUES ({parent_id}, {author}, {reply_content}, {date_created})")
        
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
                                       host='127.0.0.1',
                                       database='Project')
        cursor = cnx.cursor()

        content = request.json

        cid = content['cid']
        secName = content['section_name']

        cursor.execute(f"INSERT INTO Component (cid, compType) VALUES ({cid}, 'Section')")

        comp_id = cursor.lastrowid
        
        cursor.execute(f"INSERT INTO Section (parent, author, content, dateCreated) VALUES ({comp_id}, {cid}, {secName})")


        lect_id = loggedInUser['uid']

        cursor.execute(f"INSERT INTO ModifySection VALUES ({lect_id}, {comp_id}, {cid})")

        
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
                                       host='127.0.0.1',
                                       database='Project')
        cursor = cnx.cursor()

        content = request.json
        parent_id = content['sec_id']
        parent_cid = content['cid']
        secItemName = content['item_name']
        itemType = content['item_type']
        contentPath = content['contentPath']

        cursor.execute(f"INSERT INTO SectionItems VALUES ({parent_id}, {parent_cid}, {secItemName}, {itemType}, {contentPath})")
        item_id = cursor.lastrowid


        #add to modify items table
        lect_id = loggedInUser['uid']
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
                                       host='127.0.0.1',
                                       database='Project')
        cursor = cnx.cursor(dictionary=True) 
        
        cursor.execute(f"SELECT comp_id, secName FROM Section WHERE cid = '{cid}'")
        sections = cursor.fetchall()

        
        allContent = []

        for section in sections:
            comp_id = section['comp_id']
            section_name = section['secName']

            # get all section items for each section
            cursor.execute(f"SELECT item_id, item_name, item_type, contentPath FROM SectionItems WHERE parent_id = '{comp_id}' AND parent_cid = '{cid}'")
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

