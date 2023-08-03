from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@127.0.0.1/lbrs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = '7e908ae6-8bb1-445f-9cb9-f003fda72397'

db = SQLAlchemy(app)

from app.routes.user import users_route
from app.routes.location import locations_route
from app.routes.bus import bus_route
from app.routes.search import search_route
from app.routes.userapp import user_app_route
from app.routes.adminapp import admin_app_route




app.register_blueprint(users_route)
app.register_blueprint(locations_route)
app.register_blueprint(bus_route)
app.register_blueprint(user_app_route)
app.register_blueprint(admin_app_route)


@app.route('/home')
@app.route('/')
def home():
    path = 'Home'

    return render_template('web/index.html', path=path)


@app.errorhandler(404)
def page_not_found(e):
    path = '404'
    return render_template('404.html', path=path)




app.add_url_rule("/", endpoint="index")

with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
