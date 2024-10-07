#user_class.py

class User:
  def __init__(self, username, email, password, role):
    """
    Initialize a User object.
     
    Args:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.
        role (str): The role of the user (either 'student' or 'staff').
    """
    self.username = username
    self.email = email
    self.password = password
    self.role = role
if __name__ = "__main__":
  pass
