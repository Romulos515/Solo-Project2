from flask import render_template, request, redirect, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import event

class Attendee:
    DB = "myproject_db"
    def __init__(self, attendee_dict):
        self.user_id = attendee_dict['user_id']
        self.event_id = attendee_dict['event_id']
        self.joined_at = attendee_dict['joined_at']
        self.left_at = attendee_dict['left_at']
        self.user = []
        self.event = []


    # @staticmethod
    # def join_as_attendee(event_id, user_id):
    #     query = """
    #         Insert into attendees (event_id, user_id) 
    #         VALUES %(event_id)s, %(user_id)s)"""
    #     data = {'event_id': event_id, 'user_id': user_id}
    #     return connectToMySQL("myproject_db").query_db(query, data)

    # @staticmethod
    # def leave_as_attendee(event_id, user_id):
    #     query = """
    #         Delete from attendees 
    #         WHERE event_id = %(event_id)s AND user_id = %(user_id)s"""
    #     data = {'event_id': event_id, 'user_id': user_id}
    #     return connectToMySQL("myproject_db").query_db(query, data)

        # @classmethod
    # def get_event_for_attendees(cls, event_id):
    #     event = cls.get_one(event_id)
    #     query = """
    #         SELECT * FROM attendees 
    #         JOIN users ON users.id=attendees.user_id
    #         WHERE event_id = %(event_id)s
    #     """
    #     data = {"event_id": event_id}
    #     result = connectToMySQL(cls.DB).query_db(query, data)
    #     attendees = []
    #     for row in result:
    #         attendee_obj = attendee.Attendee(row)
    #         user_dict = {
    #             "id":  row["id"],
    #             "first_name": row["first_name"],
    #             "last_name": row["last_name"],
    #             "phone_number":  row["phone_number"],
    #             "email":  row["email"],
    #             "password":  row["password"],
    #             "created_at":  row["created_at"],
    #             "updated_at":  row["updated_at"],

    #         }
    #         user_one = user.User(user_dict)
    #         attendee_obj.user = user_one
    #         attendees.append(attendee_obj)

    #     event.attendees = attendees
    #     return event

#     @app.route('/event/enroll/<int:event_id>', methods=["GET"])
# def enroll(event_id):
#     if event.Event.enroll_user(event_id, session['user_id']) == True:
#         flash("You are already enrolled in this event.", "join_error")
#         return redirect(f"/event/{event_id}")
#     else:
#         flash("You are enrolled in this event.","success")
#         return redirect(f"/event/{event_id}")