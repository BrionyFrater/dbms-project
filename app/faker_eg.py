from faker import Faker
import random

#Check generated.sql after running this

fake = Faker()

course_names = {
    "COMP1234": "Computer Science",
    "MATH5678": "Mathematics",
    "PHYS9012": "Physics",
    "BIOL3456": "Biology",
    "CHEM7890": "Chemistry",
    "ENGL2345": "English",
    "HIST6789": "History",
    "PSYC0123": "Psychology",
    "ECON4567": "Economics",
    "ARTS8901": "Art History",
    "STAT2345": "Statistics",
    "LANG6789": "Language Studies",
    "GEOL0123": "Geology",
    "PHIL4567": "Philosophy",
    "SOCI8901": "Sociology",
    "MUSC2345": "Music",
    "ANTH6789": "Anthropology",
    "THEA0123": "Theater",
    "EDUC4567": "Education",
    "LING8901": "Linguistics",
    "ARAB2345": "Arabic Studies",
    "CHIN6789": "Chinese Studies",
    "FREN0123": "French Studies",
    "GERM4567": "German Studies",
    "ITAL8901": "Italian Studies",
    "JAPA2345": "Japanese Studies",
    "KORE6789": "Korean Studies",
    "PORT0123": "Portuguese Studies",
    "RUSS4567": "Russian Studies",
    "SPAN8901": "Spanish Studies",
    "AFRI2345": "African Studies",
    "HIND6789": "Hindi Studies",
    "INDO0123": "Indonesian Studies",
    "PERS4567": "Persian Studies",
    "TURK8901": "Turkish Studies",
    "VIET2345": "Vietnamese Studies",
    "BIOE6789": "Biomedical Engineering",
    "CIVE0123": "Civil Engineering",
    "ELEC4567": "Electrical Engineering",
    "ENVE8901": "Environmental Engineering",
    "MECH2345": "Mechanical Engineering",
    "MINE6789": "Mining Engineering",
    "SYDE0123": "Systems Design Engineering",
    "ACTS4567": "Accounting",
    "BUSI8901": "Business Administration",
    "FINA2345": "Finance",
    "MANA6789": "Management",
    "MARK0123": "Marketing"
}

deps = [
    "Humanities",
    "Science and Technology",
    "Social Sciences",
    "Law",
    "Medical Sciences",
    "Engineering" 
    
]

#lecturers
num_lecturers = 22
lecturers = [(fake.unique.random_int(min=1000, max=5000), fake.name(), random.choice(deps)) for i in range(num_lecturers)]

#Courses
num_courses = 50
courses = []

for i in range(num_courses):

    id = fake.unique.random_int(min=9200, max=9900)
    crs_code = random.choice(list(course_names.keys()))


    courses += [ (id, course_names[crs_code], crs_code)]

#Students
num_students = 200
students = [(fake.unique.random_int(min=600000000, max=699999999), fake.first_name(), fake.last_name()) for i in range(num_students)]


teaches = []

for i, lecturer in enumerate(lecturers[:20]):
    course1 = courses[i * 2][0]
    course2 = courses[i * 2 + 1][0]
    teaches.append((lecturer[0], course1))
    teaches.append((lecturer[0], course2))

    

teaches.append((lecturers[21][0], courses[44][0]))

for indx in range(40, len(courses)):
    teaches.append((lecturers[17][0], courses[indx][0]))

grades = []

for std in students:
    
    crse = random.randint(0, 49)
    num_courses = 1

    if crse <= 45:
        num_courses = random.randint(1, 5)
 
    for i in range(num_courses):
        grade = random.randint(0, 100)
        course = courses[crse + i][0]
        grades += [ (course, std[0], grade) ]



# Write SQL insert queries to a file
try:
    f = open('generated.sql', 'w')
except:
    print('An error has occurred with the file')
else:
    with f:
        # Clear the file
        f.truncate(0)
        
        # Insert queries for lecturers
        for lecturer in lecturers:
            f.write("INSERT INTO Lecturer (LecId, LecName, Department) VALUES " + str(lecturer) + ";\n")
        
        # Insert queries for courses
        for course in courses:
            f.write("INSERT INTO Course (CourseId, CourseName, CourseCode) VALUES " + str(course) + ";\n")
        
        # Insert queries for students
        for student in students:
            f.write("INSERT INTO Student (StudentID, FirstName, LastName) VALUES " + str(student) + ";\n")
        
        for teach in teaches:
            f.write("INSERT INTO Teaches (LecId, CourseId) VALUES " + str(teach) + ";\n")
        for grade in grades:
            f.write("INSERT INTO Grade (CourseId, StudentID, Grade) VALUES " + str(grade) + ";\n")

        print("FINISHED GENERATING")

