from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)


users = {
    'user1': 'password1',
    'user2': 'password2',
}


SECRET_KEY = 'your-secret-key'


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        if username not in users:
            users[username] = password
            return jsonify({"message": "Registration successful"}), 201
        else:
            return jsonify({"message": "Username already exists"}), 400
    else:
        return jsonify({"message": "Invalid input"}), 400

# Login and generate a token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        # Generate a JWT token
        token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY, algorithm='HS256')
        return jsonify({"token": token.decode('UTF-8')})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Protected route
@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"message": "Token is missing"}), 401

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({"message": f"Welcome, {data['username']}!"})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

if __name__ == '__main__':
    app.run(debug=True)
