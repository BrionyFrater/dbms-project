from faker import Faker
import random

fake = Faker()

# Generate data for the Account table
accounts_data = []
for _ in range(100000):
    fname = fake.first_name()
    lname = fake.last_name()
    phone = fake.phone_number()
    address = fake.address()
    role = random.choice(['student', 'lecturer', 'admin'])
    adminid = random.randint(1, 10) if role == 'admin' else None
    password = fake.password(length=10)
    accounts_data.append((None, fname, lname, phone, address, role, adminid, password))

# Generate data for the Admin table
admins_data = []
for i in range(1, 11):
    uid = i
    adminid = i
    date_created = fake.date_time_this_year()
    admins_data.append((uid, adminid, date_created))

# Generate data for the CreateCrse table (assuming admins create courses)
create_crse_data = []
for i in range(1, 201):
    adminid = random.randint(1, 10)
    cid = i
    date_created = fake.date_this_year()
    create_crse_data.append((adminid, cid, date_created))

# Generate data for the Course table
courses_data = []
for i in range(1, 201):
    cid = f"C{i:03}"  
    cname = fake.catch_phrase()
    date_created = fake.date_time_this_year()
    courses_data.append((cid, cname, date_created))

# Generate data for the Student table
students_data = []
for i in range(1, 100001):
    stud_id = i
    uid = i
    address = fake.address()
    password = fake.password(length=16)
    students_data.append((stud_id, uid, address, password))

# Generate data for the Enrol table
enrol_data = []
for i in range(1, 100001):
    cid = f"C{random.randint(1, 200):03}"
    uid = i
    grade = random.randint(1, 100)
    enrol_data.append((cid, uid, grade))

# Generate data for the Lecturer table
lecturers_data = []
for i in range(1, 11):
    lec_id = i
    uid = i + 100000  # Assuming lecturer UIDs start from 100001
    department = fake.job()
    password = fake.password(length=10)
    lecturers_data.append((lec_id, uid, department, password))

# Generate data for the Assigned table
assigned_data = []
for i in range(1, 100001):
    cid = f"C{random.randint(1, 200):03}"
    uid = i
    assigned_data.append((cid, uid))

# Generate data for the Member table (assuming all UIDs from 1 to 100000 are students)
members_data = [(uid, 's') for uid in range(1, 100001)]

# Output data to SQL insert statements
def generate_insert_statements(data, table_name):
    insert_statements = []
    for record in data:
        values = ", ".join([f"'{value}'" if isinstance(value, str) else str(value) for value in record])
        insert_statements.append(f"INSERT INTO {table_name} VALUES ({values});")
    return insert_statements

account_inserts = generate_insert_statements(accounts_data, 'Account')
admin_inserts = generate_insert_statements(admins_data, 'Admin')
create_crse_inserts = generate_insert_statements(create_crse_data, 'CreateCrse')
course_inserts = generate_insert_statements(courses_data, 'Course')
student_inserts = generate_insert_statements(students_data, 'Student')
enrol_inserts = generate_insert_statements(enrol_data, 'Enrol')
lecturer_inserts = generate_insert_statements(lecturers_data, 'Lecturer')
assigned_inserts = generate_insert_statements(assigned_data, 'Assigned')
member_inserts = generate_insert_statements(members_data, 'Member')

with open('data_inserts.sql', 'w') as file:
    file.write('\n'.join(account_inserts))
    file.write('\n')
    file.write('\n'.join(admin_inserts))
    file.write('\n')
    file.write('\n'.join(student_inserts))
    file.write('\n')
    file.write('\n'.join(lecturer_inserts))
    file.write('\n')
    file.write('\n'.join(member_inserts))
    file.write('\n')
    file.write('\n'.join(course_inserts))
    file.write('\n')
    file.write('\n'.join(enrol_inserts))
    file.write('\n')
    file.write('\n'.join(assigned_inserts))
    file.write('\n')
    file.write('\n'.join(create_crse_inserts))