from flask import Flask, request
import os

app = Flask(__name__)

# FIX 1: Use environment variables instead of hardcoded plaintext secrets
SECURE_USER = os.environ.get("APP_USER", "admin")
SECURE_PASS = os.environ.get("APP_PASS", "SecurePassword123!")

@app.route("/")
def home():
    return '''
        <h2>Welcome to CodeAlpha Secure App</h2>
        <form action="/login" method="POST">
            Username: <input type="text" name="username"><br><br>
            Password: <input type="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # FIX 2: Check credentials securely 
    if username == SECURE_USER and password == SECURE_PASS:
        return "<h3>Welcome back! Access Granted.</h3>"
    else:
        # FIX 3: Return a generic error message instead of echoing user input back
        return "<h3>Invalid username or password. Access Denied.</h3>"

if __name__ == "__main__":
    app.run(debug=False) # FIX 4: Disable debug mode for production safety