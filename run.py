from app import app
from models import db


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["PROPOGATE_EXCEPTIONS"] = True

with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
