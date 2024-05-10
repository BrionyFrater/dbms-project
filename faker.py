from faker import Faker
import random

fake = Faker()

# Generate data for the Account table
accounts_data = []
for uid in range(1, 100061):  # 100000 students + 50 lecturers + 10 admins
    if uid <= 100000:
        user_role = 'student'
    elif uid <= 100050:
        user_role = 'lecturer'
    else:
        user_role = 'admin'
    fname = fake.first_name()
    lname = fake.last_name()
    phoneNum = fake.phone_number()
    password = fake.password(length=10)
    accounts_data.append((uid, fname, lname, phoneNum, user_role, password))

# Generate data for the Student table
students_data = []
for uid in range(1, 100001):  
    address = fake.address()
    students_data.append((uid, address))

# Generate data for the Admin table
admins_data = []
for uid in range(100051, 100061):  
    dateCreated = fake.date_time_this_year()
    admins_data.append((uid, dateCreated))

# Generate data for the Lecturer table
lecturers_data = []
for uid in range(100001, 100021): 
    department = fake.job()
    lecturers_data.append((uid, department))

# Generate data for the Course table
courses_data = []
for cid in range(1, 201):  
    cname = fake.catch_phrase()
    dateCreated = fake.date_time_this_year()
    courses_data.append((f"C{cid:03}", cname, dateCreated))

# Generate data for the CreateCrse table
create_crse_data = []
for cid in range(1, 201):  
    admin_id = random.randint(100051, 100060)  
    dateCreated = fake.date_this_year()
    create_crse_data.append((f"C{cid:03}", admin_id, dateCreated))

# Generate data for the Component table
components_data = []
for comp_id in range(1, 201):  
    cid = f"C{random.randint(1, 200):03}"
    compType = fake.word()
    components_data.append((comp_id, cid, compType))

# Generate data for the Enrol table
enrol_data = []
for uid in range(1, 100001):  
    num_courses = random.randint(3, 6)  
    student_courses = random.sample(range(1, 201), num_courses)  
    for cid in student_courses:
        grade = random.randint(1, 100)
        enrol_data.append((f"C{cid:03}", uid, grade))

# Generate data for the Member table
members_data = []
for uid in range(1, 100061):  # 100000 students + 50 lecturers + 10 admins
    if uid <= 100000:
        user_type = 's'
    elif uid <= 100050:
        user_type = 'l'
    else:
        user_type = 'a'
    members_data.append((uid, user_type))

# Generate data for the Assigned table
assigned_data = []
for uid in range(1, 100001):  # 100000 students
    num_courses = random.randint(3, 6)  
    assigned_courses = random.sample(range(1, 201), num_courses)  
    for cid in assigned_courses:
        semester = random.randint(1, 2)  
        year = random.randint(2020, 2024)  
        assigned_data.append((f"C{cid:03}", uid, semester, year))

# Generate data for the Event table
events_data = []
for comp_id in range(1, 201):  
    cid = f"C{random.randint(1, 200):03}"
    name = fake.catch_phrase()
    description = fake.text()
    dateCreated = fake.date_this_year()
    dueDate = fake.date_between(start_date=dateCreated)
    events_data.append((comp_id, cid, name, description, dateCreated, dueDate))

# Generate data for the Forum table
forums_data = []
for comp_id in range(1, 201):  
    cid = f"C{random.randint(1, 200):03}"
    name = fake.catch_phrase()
    dateCreated = fake.date_this_year()
    forums_data.append((comp_id, cid, name, dateCreated))

# Generate data for the Thread table
threads_data = []
for _ in range(200):  
    parent = random.randint(1, 200)  
    title = fake.sentence()
    content = fake.text()
    dateCreated = fake.date_this_year()
    threads_data.append((parent, title, content, dateCreated))

# Save the SQL insert statements to a file
with open('data_inserts.sql', 'w') as file:
    for table, data in zip(['Account', 'Student', 'Admin', 'Lecturer', 'Course', 'CreateCrse', 'Component', 'Enrol', 'Member', 'Assigned', 'Event', 'Forum', 'Thread'],
                           [accounts_data, students_data, admins_data, lecturers_data, courses_data, create_crse_data, components_data, enrol_data, members_data, assigned_data, events_data, forums_data, threads_data]):
        for record in data:
            values = ", ".join([f"'{value}'" if isinstance(value, str) else str(value) for value in record])
            file.write(f"INSERT INTO {table} VALUES ({values});\n")

print("SQL insert statements saved to data_inserts.sql")
