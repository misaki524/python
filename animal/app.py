from flask import Flask, render_template
from flask_migrate import Migrate
from models import get_db
from config import Config
from routes.owners import owners_bp
from routes.pets import pets_bp
from routes.vets import vets_bp
from routes.appointments import appointments_bp

_db = get_db()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db = get_db()
    db.init_app(app)
    Migrate(app, db)

    # Blueprint 登録
    app.register_blueprint(owners_bp, url_prefix="/owners")
    app.register_blueprint(pets_bp, url_prefix="/pets")
    app.register_blueprint(vets_bp, url_prefix="/vets")
    app.register_blueprint(appointments_bp, url_prefix="/appointments")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

app = create_app()


