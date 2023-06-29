from flask import render_template, request, redirect, session, flash, url_for
from flask_app import app
from flask_app.models import event, user, attendee
from flask_app.models.event import Event
from datetime import datetime


@app.route('/event/create', methods=['GET'])
def create_event_form():
    # users = user.User.get_all  users=users()
    return render_template("create_event.html")

@app.route('/event/create', methods=['POST'])
def create_event():
    event_dict = request.form
    if not Event.validate_event(event_dict):
        return redirect(url_for('create_event_form'))
    else:
        session["show_success"] = True
    data = {
        "name": request.form["name"],
        "date": request.form["date"],
        "address": request.form["address"],
        "description": request.form["description"],
        "event_duration": request.form["event_duration"],
        "user_id": session['user_id']
    }
    newly_created_event_id = event.Event.create_event(data)
    return redirect(f"/event/{newly_created_event_id}")



@app.route('/event/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    event_record = event.Event.get_event_with_user(event_id)
    events = event.Event.get_event_with_attendees(event_id) 
    user_joined_event = False
    for attendee in events.attendees:
        if attendee.user_id == session['user_id']:
            user_joined_event = True
            break
    return render_template("view_event.html", events = events , event_record=event_record, event_id=event_id, user_joined_event=user_joined_event)

#enroll route.
@app.route('/event/enroll/<int:event_id>', methods=["GET"])
def enroll(event_id):
    user_id = session['user_id']
    flash("Thank you for your heart of service!", "success")
    event.Event.enroll_user(event_id, user_id)
    return redirect(f"/event/{event_id}")

@app.route('/event/leave/<int:event_id>', methods=["GET"])
def leave_event(event_id):
    user_id = session['user_id']
    flash("You have left the event", "join_error")
    event.Event.un_enroll_user(event_id, user_id)
    return redirect(f"/event/{event_id}")

@app.route("/edit/event/<int:event_id>", methods=["GET"])
def edit_event(event_id):
    event_return = event.Event.get_event_with_user(event_id)
    return render_template("edit_event.html", event_return=event_return)


@app.route("/edit/event/<int:event_id>", methods=["POST"])
def update_event(event_id):
    event_dict = request.form
    if not Event.validate_event(event_dict):
        return redirect(f"/edit/event/{event_id}")
    else:
        session["show_success"] = True
        data={
            "id": event_id,
            "name": request.form["name"],
            "date": request.form["date"],
            "address": request.form["address"],
            "description": request.form["description"],
            "event_duration": request.form["event_duration"],
            "user_id": session["user_id"]
        }
    Event.update_event(data)
    return redirect("/dashboard")

@app.route("/delete/event/<int:event_id>", methods=["GET"])
def delete_event(event_id):
    Event.delete_event(event_id)
    return redirect("/dashboard")

