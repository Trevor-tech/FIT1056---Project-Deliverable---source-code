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
  def verification(self, identifier, password):
    """
    Verify a user's credentials.
    
    Args:
      identifier (str): The username or email of the user.
      password (str): The password of the user.

    Returns:
      bool: True if the user's credentials are valid, False otherwise.
    """
      return (identifier in [self.username, self.email] and 
        self.password == password and 
        self.role in ['student', 'staff'])

# Example usage
user = User('john_doe', 'john@example.com', 'password123', 'student')

print(user.verification('john_doe', 'password123'))  # Output: True
print(user.verification('john@example.com', 'password123'))  # Output: True
print(user.verification('jane_doe', 'wrong_password'))  # Output: False
print(user.verification('unknown_user', 'password'))  # Output: False
