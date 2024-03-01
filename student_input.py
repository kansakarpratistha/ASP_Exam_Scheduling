from main import Student, StudentCourses

class StudentInput:
    def addStudent(self, students_data):
        students_data = students_data.to_dict(orient="records")
        students = []
        for item in students_data:
            students.append(Student(student_id = str(item['ID']), name = item['Name'], module_code = item['Module']))
        return students

    def addStudentCourse(self, student_courses_data):
        student_courses_data = student_courses_data.to_dict(orient="records")
        student_courses = []
        for item in student_courses_data:
            student_courses.append(StudentCourses(student_id=str(item['ID']), course_id=item['Course']))
        return student_courses