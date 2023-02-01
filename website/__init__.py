from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY, DB_URI
from flask_login import LoginManager

app = Flask(__name__)

@app.template_filter()
def to_str(value):
    return str(value)


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.secret_key = SECRET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    print("DB Initialized Successfully")

    
    from .views import views
    app.register_blueprint(views)

    with app.app_context():
        # db.drop_all()
        db.create_all()
        db.session.commit()

    from .models.user import User
    from .models.library import Library
    from .models.userType import UserType

    login_manager = LoginManager()
    login_manager.login_view = 'views.index'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        
        id = UserType.query.get(int(user_id))

        if id:
            return id
        else:
            return None


    return app