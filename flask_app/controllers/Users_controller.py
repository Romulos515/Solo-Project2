from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import event, user
from flask_app.models.user import User
from flask_app.models.event import Event
from datetime import datetime


@app.route('/dashboard')
def all_events():
    if "user_id" not in session:
        flash("Please login first!!", "error")
        return redirect("/login")
    data={
        'id': session['user_id']
    }
    session['user_id']
    return render_template("dashboard.html", all_events = Event.get_events_with_users(),user=User.get_one(data))

@app.route('/user_profile')
def user_profile():
    if "user_id" not in session:
        flash("Please login first!!", "error")
        return redirect("/login")
    data={
        'id': session['user_id']
    }
    session['user_id']
    return render_template("user_profile.html", user=User.get_one(data))