from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re


# THIS IS COPIED FROM THE PLATFORM: PATTERN VALIDATION FOR EMAIL VALIDATION
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# THIS IS DATA FROM OUR DATABASE
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


# THIS METHOD CREATES A USER INTO OUR DATABASE
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO user (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results



# CREATES THE VALIDATION METHOD FOR THE REGISTRATION FORM
    @staticmethod
    def validate_user(user):
        is_valid = True

        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", "registration")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "registration")
            is_valid = False

# THIS CHECKS IF EMAIL HAS VALID INPUT
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", "registration")
            is_valid = False

# THIS CHECKS IF EMAIL IS ALREADY IN USE
        if (re.fullmatch(EMAIL_REGEX, user['email'])):
            this_user = {
                'email' : user['email']
            }
            results = User.check_database(this_user)
            if len(results) != 0:
                flash("Email is already in use, please use a different email.", "registration")
                is_valid = False

# THIS CHECKS THE PASSWORD LENGTH
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "registration")
            is_valid = False

# THIS CHECKS FOR PASSWORD TO HAVE 1 DIGIT
        if(re.search('[0-9]', user['password'])== None):
            flash("Password requires at least 1 digit", "registration")
            is_valid = False

# THIS CHECKS FOR PASSWORD TO HAVE 1 UPPERCASE LETTER
        if(re.search('[A-Z]', user['password'])== None):
            flash("Password requires at least 1 uppercase letter", "registration")
            is_valid = False


# THIS CHECKS THAT PASSWORD AND PASSWORD CONFIRMATION MATCH
        if (user['password'] != user['confirm_password']):
            flash("Passwords do not match!", "registration")
            is_valid = False
        return is_valid
    

# CREATES THE VALIDATION METHOD FOR THE LOGIN FORM
    @staticmethod
    def validate_login(user):
        is_valid = True
        
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", "login")
            is_valid = False
        if len(user['email']) < 3:
            flash("Email must be at least 3 characters.", "login")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "login")
            is_valid = False
        return is_valid
    

# THIS CLASSMETHOD IS TO CHECK IF EMAIL IS ALREADY IN USE
    @classmethod
    def check_database(cls, data):
        query="SELECT * FROM user WHERE email = %(email)s"

        results = connectToMySQL(DATABASE).query_db(query, data)

        return results


# THIS CLASSMETHOD IS TO GET DATA OF ONE USER ID AND SAVE IT TO A VARIABLE
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM user WHERE id = %(user_id)s"

        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])
    

# THIS READS ONE USER FROM THE DATABASE BY EMAIL
    @classmethod
    def read_one_user_by_email(cls, data):
        query = "SELECT * FROM user WHERE email = %(email)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        
        if not result:
            return None
        
        return User(result[0])