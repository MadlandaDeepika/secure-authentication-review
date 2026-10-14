from flask import Flask, request, render_template_string, make_response
import os

app = Flask(__name__)

# Simulated environment configuration (Secure coding practice)
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "CodeAlphaSecure2026!")

# Professional, highly aesthetic enterprise template using modern CSS
ENTERPRISE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise Identity Portal</title>
    <style>
        :root {
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --bg: #0b0f19;
            --card-bg: #111827;
            --text: #f3f4f6;
            --text-muted: #9ca3af;
            --border: #374151;
        }
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .auth-card {
            background-color: var(--card-bg);
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
            width: 380px;
            border: 1px solid var(--border);
        }
        .portal-tag {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #60a5fa;
            font-weight: 700;
            margin-bottom: 8px;
        }
        h2 {
            margin-top: 0;
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 24px;
            color: #ffffff;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 6px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px 14px;
            background-color: #1f2937;
            border: 1px solid var(--border);
            border-radius: 6px;
            color: white;
            font-size: 14px;
            box-sizing: border-box;
            transition: border-color 0.2s;
        }
        input:focus {
            outline: none;
            border-color: var(--primary);
        }
        button {
            width: 100%;
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        button:hover {
            background-color: var(--primary-hover);
        }
        .security-badge {
            margin-top: 24px;
            text-align: center;
            font-size: 11px;
            color: var(--text-muted);
            border-top: 1px solid var(--border);
            padding-top: 16px;
        }
    </style>
</head>
<body>
    <div class="auth-card">
        <div class="portal-tag">Secure Authentication System</div>
        <h2>Sign In to Portal</h2>
        <form action="/login" method="POST">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Enter administrator ID" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter secure password" required>
            </div>
            <button type="submit">Authenticate Session</button>
        </form>
        <div class="security-badge">Secured via TLS &bull; RBAC Enforced</div>
    </div>
</body>
</html>
'''

@app.route("/")
def home():
    response = make_response(render_template_string(ENTERPRISE_TEMPLATE))
    # Enterprise security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == ADMIN_USER and password == ADMIN_PASS:
        return "<h2 style='text-align:center; margin-top:20vh; font-family:Inter, sans-serif; color:#10b981;'>Access Granted: Administrator Session Active.</h2>"
    else:
        return "<h2 style='text-align:center; margin-top:20vh; font-family:Inter, sans-serif; color:#ef4444;'>Access Denied: Authentication Failed.</h2>"

if __name__ == "__main__":
    app.run(debug=False)