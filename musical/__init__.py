from flask import Flask, redirect, url_for
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_class=None):
    """
    Application factory: creates and configures the Flask app.
    """
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musical.db'

    db.init_app(app)
    ma.init_app(app)

    from musical import models  
    from musical import logic

    from musical.routes import edit_bp, view_bp
    app.register_blueprint(edit_bp, url_prefix='/edit')
    app.register_blueprint(view_bp, url_prefix='/view')

    @app.route("/")
    def root():
        return redirect(url_for("view.index"))

    with app.app_context():
        db.create_all()
        logic.import_students_from_csv("cast.csv")
    
    return app
