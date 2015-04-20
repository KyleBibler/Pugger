from flask import *
import os
#from flask_login import login_required, logout_user, login_user, current_user, LoginManager
from models import db, User, Event, init_db


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'
db_session = db.session

@app.route('/init-events')
def init():
    init_db()

@app.route('/')
def index():
    return render_template("index.html", title=None)


@app.route('/events/event-list.json')
def event_list():
    events = []
    for i in Event.query.all():
        events += [i.serialize()]
    return jsonify(events=events)


# def init_login():
#     login_manager = LoginManager()
#     login_manager.init_app(app)
#     login_manager.login_view = "/login"
#
#     # Create user loader function
#     @login_manager.user_loader
#     def load_user(user_id):
#         return db.session.query(User).get(user_id)

# init_login()


if __name__ == '__main__':
    app.run()
