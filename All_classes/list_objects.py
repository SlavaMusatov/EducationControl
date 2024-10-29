from single_objects import *

class StudentsGroup():
    def __init__(self, group_name):
        self.group_name = group_name
        self.start_date = None

    def set_students_list(self, lst):
        self.students_list = lst
        self.value = [Student(num) for num in lst]



class Course():
    def __init__(self, course_name):
        self.name = course_name

    def set_stages(self, lst):
        self.stages_list = lst
        self.value = [StageOfCourse(n) for n in lst]

class Statistics():
    def __init__(self, lst):
        self.statistics_list = lst
        self.value = [Report(nme) for nme in lst]
