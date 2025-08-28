from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

#-----------------------------------
# CONFIGURAÇÃO INICIAL
#-----------------------------------

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#-----------------------------------
# MODELS
#-----------------------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=True)
    password = db.Column(db.String(20), nullable=False)
    tasks = db.relationship("Task", backref="user", lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="Pendente")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

#-----------------------------------
# ROTAS
#-----------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

#-----------------------------------
# CRIAR BANCO NA PRIMEIRA EXECUÇÃO
#-----------------------------------

if __name__ == "__main__":
    if not os.path.exists("database.db"):
        with app.app_context():
            db.create_all()
    app.run(debug=True)