class Student():
    def __init__(self, student_id):
        self.student_id = student_id
        self.second_name = None
        self.first_name = None
        self.third_name = None
        self.birth_date = None
        self.start_date = None
        self.end_date = None
        self.status = None

class StageOfCourse():
    def __init__(self, stage_name):
        self.name = stage_name
        self.description = None

class Report():
    def __init__(self, report_name):
        self.name = report_name
        self.value = None