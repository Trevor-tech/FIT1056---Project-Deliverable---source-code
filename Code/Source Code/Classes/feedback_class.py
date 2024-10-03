from assignment_class import Assignment

class Feedback(Assignment):
    def __init__(self, course_ID, course_name, assignment_ID, title, due_date, feedback_ID, comments, grades):
        super().__init__(course_ID, course_name, assignment_ID, title, due_date)
        self.feedback_ID = feedback_ID
        self.comments = comments
        self.grades = grades
    
    def add_comments(self):
        pass
    
    def assign_grade(self):
        pass 
