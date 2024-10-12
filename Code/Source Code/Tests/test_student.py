# Standard library imports
import sys
sys.path.append("../app")

# Related third party imports
import pytest

# Local application/library specific imports
from classes.student_class import Student

def test_authenticate():
    assert Student.authenticate("willeykong", "password123") == True
    assert Student.authenticate("adamriz", "password123") == False