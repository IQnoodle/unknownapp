class EnrollmentSystem:
    def __init__(self, students, courses):
        self.students = students
        self.courses = courses

    def register_course(self, student_id, course_code):
        # 1. Basic Checks
        student = self.students.get(student_id)
        course = self.courses.get(course_code)
        
        if not student: return "Error: Student not found."
        if not course: return "Error: Course not found."
        if course_code in student['enrolled_courses']:
            return f"Error: Already enrolled in {course_code}."

        # 2. Capacity Check
        if len(course['enrolled_students']) >= course['capacity']:
            return "Error: Course is full."

        # 3. Prerequisite Check
        for prereq in course.get('prerequisites', []):
            if prereq not in student.get('completed_courses', []):
                return f"Error: Prerequisite {prereq} not met."

        # 4. Time Conflict Check
        new_slot = course['time_slot']
        for enrolled_code in student['enrolled_courses']:
            enrolled_course = self.courses.get(enrolled_code)
            if self._has_conflict(new_slot, enrolled_course['time_slot']):
                return f"Error: Schedule conflict with {enrolled_code}."

        # 5. Perform Enrollment
        student['enrolled_courses'].append(course_code)
        course['enrolled_students'].append(student_id)
        return f"Success: Enrolled in {course_code}."

    def _has_conflict(self, slot1, slot2):
        # Simplified overlap logic: share days and overlap time
        shared_days = set(slot1['days']) & set(slot2['days'])
        if not shared_days: return False
        
        return (slot1['start'] < slot2['end'] and slot2['start'] < slot1['end'])