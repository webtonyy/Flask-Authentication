from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import pymysql

conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'admin123',
    db = 'mysql'
)


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud'
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
#view login
login_manager.login_view = 'login'
#Session <- conexão ativa

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username and password:

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Successfull authentication"})

    return jsonify({"message": "Invalid credentials"}), 400

@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Successfull logged out"})

@app.route("/user", methods=['POST'])
def create_user():

    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"User registered successfully"})

    return jsonify({"message":"Invalid data"}), 401

@app.route("/user/<int:id>", methods=['GET'])
def read_user(id):
    user = User.query.get(id)
    
    if user:
        return {"username":user.username}

    return jsonify({"message":"User not found"}), 404

@app.route("/user/<int:id>", methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    data = request.json
    
    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"message":f"User {id} updated successfully "})

    return jsonify({"message":"User not found"}), 404

@app.route("/user/<int:id>", methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    
    if user and id != current_user.id:
        db.session.delete(user)
        db.session.commit(user)
        return jsonify({"message":"User deleted"})
    return jsonify({"message":"User not found"}), 404



if __name__ == '__main__':
    app.run(debug=True)