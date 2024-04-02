from main import Course

class CourseInput:
    def addCourse(self, courses_data):
        courses_data = courses_data.to_dict(orient="records")
        courses = []
        for item in courses_data:
            courses.append(Course(course_id=item['Course_id'], examiner_id=item['Examiner']))
        return courses
    
