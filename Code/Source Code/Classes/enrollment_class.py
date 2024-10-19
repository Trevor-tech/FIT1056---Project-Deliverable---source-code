from classes.course_class import Course

class Enrollment(Course):
    """
    A class representing a student's enrollment in a course, inheriting from the Course class.

    Attributes:
        course_ID (str): The unique identifier for the course.
        last_name (str): The student's last name.
        first_name (str): The student's first name.
        enrolment_date (str): The date of enrollment.
        credit (str): The number of credits for the course.
        enrolled_units (list): A list of tuples containing enrolled unit IDs and names.

    Methods:
        __init__(self, course_ID, last_name, first_name, enrolment_date, credit)
        enroll_unit(self, unit_ID, unit_name)
        get_enrolment_status(self)
    """

    def __init__(self, course_ID, last_name, first_name, enrolment_date, credit):
        """
        Initialize an Enrollment object.

        Args:
            course_ID (str): The unique identifier for the course.
            last_name (str): The student's last name.
            first_name (str): The student's first name.
            enrolment_date (str): The date of enrollment.
            credit (str): The number of credits for the course.
        """
        super().__init__(course_ID, f"{last_name} {first_name}")
        self.last_name = last_name
        self.first_name = first_name
        self.enrolment_date = enrolment_date
        self.credit = credit

    def enroll_unit(self, unit_ID, unit_name):
        """
        Enroll a student in a unit.

        Args:
            unit_ID (str): The unique identifier for the unit.
            unit_name (str): The name of the unit.

        Prints:
            A message indicating successful enrollment or if the unit is already enrolled.
        """
        if unit_ID not in self.enrolled_units:
            self.enrolled_units.append((unit_ID, unit_name))
            print(f"Unit {unit_name} (ID: {unit_ID}) enrolled successfully.")
        else:
            print(f"Unit {unit_name} (ID: {unit_ID}) is already enrolled.")

    def get_enrolment_status(self):
        """
        Display the enrollment status of the student.

        Prints:
            A list of enrolled units with their IDs and names.
        """
        print("Enrolled Units:")
        for unit in self.enrolled_units:
            print(f"Unit ID: {unit[0]}, Unit Name: {unit[1]}")

if __name__ == "__main__":
    enrollment = Enrollment("C001", "Doe", "John", "2024-01-01", "6")
    print(enrollment.course_ID)
    print(enrollment.last_name)
    print(enrollment.first_name)
    print(enrollment.enrolment_date)
    print(enrollment.credit)
