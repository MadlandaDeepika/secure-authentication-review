
import os
import hmac
import secrets

from flask import (
    Flask,
    request,
    session,
    redirect,
    url_for,
    render_template_string,
    abort,
)
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Load credentials securely from environment variables.
secret_key = os.environ.get("FLASK_SECRET_KEY")
admin_user = os.environ.get("APP_USER")
password_hash = os.environ.get("APP_PASSWORD_HASH")

if not secret_key or not admin_user or not password_hash:
    raise RuntimeError(
        "Set FLASK_SECRET_KEY, APP_USER, and APP_PASSWORD_HASH "
        "before starting the application."
    )

app.config.update(
    SECRET_KEY=secret_key,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE") == "1",
)

# Modern, responsive login page.
LOGIN_PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Secure Authentication | CodeAlpha</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            font-family: "Segoe UI", Arial, sans-serif;
            color: #202944;
            background: linear-gradient(
                135deg, #eef2ff, #f8faff, #e0e7ff
            );
        }

        .login-card {
            width: 100%;
            max-width: 420px;
            padding: 38px 32px;
            background: white;
            border: 1px solid #e7eaf4;
            border-radius: 22px;
            box-shadow: 0 20px 60px rgba(40, 55, 100, 0.12);
        }

        .logo {
            width: 58px;
            height: 58px;
            margin: 0 auto 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 18px;
            color: white;
            font-size: 27px;
            background: linear-gradient(135deg, #6366f1, #4338ca);
        }

        h1 {
            margin: 0;
            text-align: center;
            font-size: 26px;
        }

        .subtitle {
            margin: 10px 0 28px;
            text-align: center;
            color: #747d94;
            font-size: 14px;
            line-height: 1.6;
        }

        label {
            display: block;
            margin: 18px 0 8px;
            font-size: 13px;
            font-weight: 600;
        }

        input {
            width: 100%;
            padding: 13px 14px;
            border: 1px solid #dce1ed;
            border-radius: 10px;
            font-size: 15px;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        input:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 3px #6366f122;
        }

        button {
            width: 100%;
            margin-top: 24px;
            padding: 14px;
            border: none;
            border-radius: 10px;
            background: #4f46e5;
            color: white;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s, transform 0.2s;
        }

        button:hover {
            background: #3730a3;
            transform: translateY(-1px);
        }

        .error {
            padding: 11px 12px;
            border-radius: 9px;
            background: #fff1f2;
            color: #be123c;
            font-size: 13px;
        }

        .footer {
            margin-top: 25px;
            text-align: center;
            color: #8991a5;
            font-size: 12px;
        }

        @media (max-width: 420px) {
            .login-card {
                padding: 30px 22px;
            }
        }
    </style>
</head>
<body>
    <main class="login-card">
        <div class="logo" aria-hidden="true">&#128274;</div>

        <h1>Welcome back</h1>

        <p class="subtitle">
            Secure Authentication Portal<br>
            Sign in to continue to your account.
        </p>

        {% if error %}
            <p class="error" role="alert">{{ error }}</p>
        {% endif %}

        <form action="{{ url_for('login') }}" method="post">
            <input
                type="hidden"
                name="csrf_token"
                value="{{ csrf_token }}"
            >

            <label for="username">Username</label>
            <input
                id="username"
                type="text"
                name="username"
                placeholder="Enter your username"
                autocomplete="username"
                required
            >

            <label for="password">Password</label>
            <input
                id="password"
                type="password"
                name="password"
                placeholder="Enter your password"
                autocomplete="current-password"
                required
            >

            <button type="submit">Sign in securely &#8594;</button>
        </form>

        <p class="footer">
            Protected sign-in &middot; CodeAlpha Security Project
        </p>
    </main>
</body>
</html>
"""

# Simple authenticated dashboard.
DASHBOARD_PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dashboard | CodeAlpha</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            font-family: "Segoe UI", Arial, sans-serif;
            color: #202944;
            background: linear-gradient(135deg, #eef2ff, #f8faff);
        }

        .dashboard-card {
            width: 100%;
            max-width: 520px;
            padding: 42px 32px;
            text-align: center;
            background: white;
            border: 1px solid #e7eaf4;
            border-radius: 22px;
            box-shadow: 0 20px 60px rgba(40, 55, 100, 0.12);
        }

        .success-icon {
            width: 64px;
            height: 64px;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: #dcfce7;
            color: #15803d;
            font-size: 32px;
        }

        h1 {
            margin: 0 0 12px;
            font-size: 27px;
        }

        p {
            color: #747d94;
            line-height: 1.7;
        }

        .status {
            display: inline-block;
            margin: 12px 0;
            padding: 8px 14px;
            border-radius: 30px;
            background: #ecfdf5;
            color: #047857;
            font-size: 13px;
            font-weight: 600;
        }

        button {
            margin-top: 22px;
            padding: 13px 28px;
            border: none;
            border-radius: 10px;
            background: #4f46e5;
            color: white;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
        }

        button:hover {
            background: #3730a3;
        }
    </style>
</head>
<body>
    <main class="dashboard-card">
        <div class="success-icon" aria-hidden="true">&#10003;</div>

        <h1>Welcome, {{ username }}!</h1>
        <p>You have successfully signed in to the authentication demo.</p>

        <div class="status">Secure session active</div>

        <form action="{{ url_for('logout') }}" method="post">
            <input
                type="hidden"
                name="csrf_token"
                value="{{ csrf_token }}"
            >
            <button type="submit">Sign out</button>
        </form>
    </main>
</body>
</html>
"""


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'unsafe-inline'; "
        "form-action 'self'; "
        "base-uri 'none'; "
        "frame-ancestors 'none'"
    )
    return response


def create_csrf_token():
    token = secrets.token_urlsafe(32)
    session["csrf_token"] = token
    return token


def valid_csrf_token():
    submitted = request.form.get("csrf_token", "")
    expected = session.get("csrf_token", "")

    return bool(expected) and hmac.compare_digest(submitted, expected)


@app.route("/")
def home():
    if session.get("authenticated") is True:
        return redirect(url_for("dashboard"))

    csrf_token = session.get("csrf_token")
    if not csrf_token:
        csrf_token = create_csrf_token()

    return render_template_string(
        LOGIN_PAGE,
        error=None,
        csrf_token=csrf_token,
    )


@app.route("/login", methods=["POST"])
def login():
    if not valid_csrf_token():
        abort(
            400,
            description="Invalid request. Reload the page and try again.",
        )

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if (
        hmac.compare_digest(username, admin_user)
        and check_password_hash(password_hash, password)
    ):
        # Clear the old session and create a fresh CSRF token.
        session.clear()
        session["authenticated"] = True
        session["username"] = admin_user
        create_csrf_token()

        return redirect(url_for("dashboard"))

    # Use a fresh token after an unsuccessful login attempt.
    csrf_token = create_csrf_token()

    return render_template_string(
        LOGIN_PAGE,
        error="Invalid username or password. Please try again.",
        csrf_token=csrf_token,
    ), 401


@app.route("/dashboard")
def dashboard():
    if session.get("authenticated") is not True:
        return redirect(url_for("home"))

    csrf_token = session.get("csrf_token")
    if not csrf_token:
        csrf_token = create_csrf_token()

    return render_template_string(
        DASHBOARD_PAGE,
        username=session.get("username", "User"),
        csrf_token=csrf_token,
    )


@app.route("/logout", methods=["POST"])
def logout():
    if not valid_csrf_token():
        abort(
            400,
            description="Invalid request. Reload the page and try again.",
        )

    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    # Local development only. Do not expose this server publicly.
    app.run(debug=False)
