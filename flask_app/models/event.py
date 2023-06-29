from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, event, attendee
from datetime import datetime
from flask_app.models.attendee import Attendee
from flask_app.models.user import User



class Event:
    DB = "myproject_db"

    def __init__(self, event_dict):
        self.id = event_dict["id"]
        self.name = event_dict["name"]
        self.date = event_dict["date"]
        self.address = event_dict["address"]
        self.description = event_dict["description"]
        self.event_duration = event_dict["event_duration"]
        self.created_at = event_dict["created_at"]
        self.updated_at = event_dict["updated_at"]
        self.User_id = event_dict["User_id"]
        self.user = None
        self.attendees = []

    @classmethod
    def create_event(cls, data):
        query = "INSERT INTO events (name, date, address, description,event_duration, user_id) VALUES (%(name)s, %(date)s, %(address)s,%(description)s,%(event_duration)s,%(user_id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)


# Enrolls a user to an event
    @classmethod
    def enroll_user(cls, event_id, user_id):
        sql = """INSERT INTO attendees (event_id, user_id, joined_at) VALUES (%(event_id)s, %(user_id)s, NOW())"""
        data = {"event_id": event_id, "user_id":user_id}
        results = connectToMySQL(cls.DB).query_db(sql, data)
        return results
    

    @classmethod
    def un_enroll_user(cls, event_id, user_id):
        sql = """DELETE FROM attendees WHERE event_id=%(event_id)s AND user_id=%(user_id)s"""
        data = {"event_id": event_id, "user_id":user_id}
        results = connectToMySQL(cls.DB).query_db(sql, data)
        return results

    @classmethod
    def get_one(cls, event_id):
        query = "SELECT * FROM events WHERE id=%(event_id)s"
        data = {"event_id": event_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

#gets all attendees for an event
    @classmethod
    def get_event_with_attendees(cls, event_id):
        events = cls.get_one(event_id)
        query = """SELECT * FROM attendees
        JOIN users ON users.id=attendees.user_id
        WHERE event_id=%(event_id)s
        """
        data = {"event_id": event_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        attendees = []
        for row in result:
            attendee_object = attendee.Attendee(row)
            user_dict = {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "phone_number": row["phone_number"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            user_object = user.User(user_dict)
            attendee_object.user = user_object
            attendees.append(attendee_object)
            events.attendees = attendees
        return events

# renders View_event with creator and information
    @classmethod
    def get_event_with_user(cls, event_id):
        sql = """
            SELECT events.*, users.* FROM events 
            JOIN users ON events.user_id=users.id
            WHERE events.id=%(id)s
            """
        data = {"id": event_id}
        results = connectToMySQL(cls.DB).query_db(sql, data)
        event_var = cls(results[0])
        user_dict = {
            "id": results[0]["users.id"],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            "email": results[0]["email"],
            "phone_number": results[0]["phone_number"],
            "password": results[0]["password"],
            "created_at": results[0]["users.created_at"],
            "updated_at": results[0]["users.updated_at"],
            "User_id": results[0]["User_id"]
        }
        user_object = user.User(user_dict)
        event_var.user = user_object
        return event_var

# used for dashboard rendering
    @classmethod
    def get_events_with_users(cls):
        sql = """
            SELECT * FROM events
            JOIN users ON users.id=events.user_id
        """
        results = connectToMySQL(cls.DB).query_db(sql)
        all_events = []
        for row_in_db in results:
            event = cls(row_in_db)
            user_dict = {
                "id": row_in_db["users.id"],
                "first_name": row_in_db["first_name"],
                "last_name": row_in_db["last_name"],
                "email": row_in_db["email"],
                "phone_number": row_in_db["phone_number"],
                "password": row_in_db["password"],
                "created_at": row_in_db["users.created_at"],
                "updated_at": row_in_db["users.updated_at"],
            }
            user_object = user.User(user_dict)
            event.user = user_object
            all_events.append(event)
        return all_events
    
    @classmethod
    def delete_event(cls, event_id):
        query = "DELETE FROM event WHERE events.id=%(id)s"
        data = {"id": event_id}
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def update_event(cls, data):
        query = "UPDATE events SET name=%(name)s, date=%(date)s, address=%(address)s, description=%(description)s, event_duration=%(event_duration)s, user_id=%(user_id)s WHERE events.id=%(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_event(data):
        if len(data["name"]) == 0:
            flash("Name field is required", "validate_error")
            return False
        elif len(data["name"]) < 3:
            flash("Please enter a longer name", "validate_error")
            return False
        if datetime.strptime(data["date"], "%Y-%m-%dT%H:%M") < datetime.now():
            flash("Please enter a valid date", "validate_error")
            return False
        if "address" not in data or len(data["address"]) == 0:
            flash("Address field is required", "validate_error")
            return False
        if "description" not in data or len(data["description"]) == 0:
            flash("Description field is required", "validate_error")
            return False
        if len(data["description"]) < 3:
            flash("Please enter a longer Description", "validate_error")
            return False
        if len(data["event_duration"]) == 0:
            flash("Event duration field is required", "validate_error")
        
        return True
