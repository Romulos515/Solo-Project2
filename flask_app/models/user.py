from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import event, user
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "myproject_db"
    def __init__(self, user_dict):
        self.id = user_dict["id"]
        self.first_name =user_dict["first_name"]
        self.last_name =user_dict["last_name"]
        self.phone_number = user_dict["phone_number"]
        self.email = user_dict["email"]
        self.password = user_dict["password"]
        self.created_at = user_dict["created_at"]
        self.updated_at = user_dict["updated_at"]
        self.events = []
        self.attendees = []

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        result = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user_dict in result:
            users.append(cls(user_dict))

        return users
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name ,last_name, phone_number ,email , password) VALUES (%(first_name)s,%(last_name)s, %(phone_number)s,%(email)s, %(password)s)"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    # many to many relationship
    @classmethod
    def get_user_with_events(cls, data):
        sql= """ SELECT * FROM users 
            LEFT JOIN attendees on attendees.user_id = users.id
            LEFT JOIN events on attendees.event_id = events.id
            WHERE users.id=%(id)s"""
        result = connectToMySQL(cls.DB).query_db(sql, data)
        user = cls(result[0])
        for event_in_DB in result[1:]:
            event_data = {
                "id": event_in_DB["events.id"],
                "name": event_in_DB["name"],
                "date": event_in_DB["date"],
                "address": event_in_DB["address"],
                "description": event_in_DB["description"],
                "event_duration": event_in_DB["event_duration"],
                "created_at": event_in_DB["events.created_at"],
                "updated_at": event_in_DB["events.updated_at"]
            }
            user.events.append(event.Event(event_data))
        return user

    @staticmethod
    def validate_user(data):
        if "first_name" not in data or len(data["first_name"]) == 0:
            flash("First name field is required", "reg_error")
            return False
        if len(data["first_name"]) < 3:
            flash("Please enter a longer First Name", "reg_error")
            return False
        if "last_name" not in data or len(data["last_name"]) == 0:
            flash("Last name field is required", "reg_error")
            return False
        if len(data["last_name"]) < 3:
            flash("Please enter a longer Last Name", "reg_error")
            return False
        if "phone_number" not in data or len(data["phone_number"]) == 0:
            flash("Please enter a phone number", "reg_error")
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", "reg_error")
            return False
        if "email" not in data or len(data["email"]) == 0:
            flash("email field is required", "reg_error")
            return False
        
        return True

