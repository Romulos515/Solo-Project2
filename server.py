from flask_app import app
import flask_app.controllers.index_controller
import flask_app.controllers.Events_controller
import flask_app.controllers.Users_controller
import flask_app.controllers.auth_controller

if __name__ == "__main__":
    app.run(debug=True, port=5001)