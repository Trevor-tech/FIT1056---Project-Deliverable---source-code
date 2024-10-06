from Classes.assignment_class import Assignment

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

if __name__ == "__main__": 
    feedback = Feedback("C001", "Mathematics", "A001", "Assignment 1", "2024-01-01", "F001", "Good work", "100")
    print(feedback.course_ID)
    print(feedback.course_name)
    print(feedback.assignment_ID)
    print(feedback.title)
    print(feedback.due_date)
    print(feedback.feedback_ID)
    print(feedback.comments)
    print(feedback.grades)
