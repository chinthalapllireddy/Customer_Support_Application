from flask import Flask, render_template, request, jsonify, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MySQL configuration for XAMPP
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chat_support'
mysql = MySQL(app)

# In-memory messages list for demo purposes.
messages = []

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Superadmin Login
@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
        admin = cursor.fetchone()
        if admin:
            session['admin'] = admin['username']
            return redirect('/dashboard_admin')
    return render_template('login_admin.html')

# Agent Login
@app.route('/login_agent', methods=['GET', 'POST'])
def login_agent():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM agents WHERE username=%s AND password=%s", (username, password))
        agent = cursor.fetchone()
        if agent:
            session['agent'] = agent['username']
            return redirect('/chat_agent')
    return render_template('login_agent.html')

# Admin Dashboard
@app.route('/dashboard_admin')
def dashboard_admin():
    if 'admin' not in session:
        return redirect('/login_admin')
    return render_template('dashboard_admin.html')

# Create Agent (accessible by admin only)
@app.route('/create_agent', methods=['GET', 'POST'])
def create_agent():
    if 'admin' not in session:
        return redirect('/login_admin')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if agent exists already
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM agents WHERE username=%s", (username,))
        existing = cursor.fetchone()
        if existing:
            return "Agent username already exists. Choose another.", 400
        # Insert new agent
        cursor.execute("INSERT INTO agents (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        return redirect('/dashboard_admin')
    
    return render_template('create_agent.html')

# User Chat Page (no login)
@app.route('/chat_user')
def chat_user():
    return render_template('chat_user.html')

# Agent Chat Page (requires login)
@app.route('/chat_agent')
def chat_agent():
    if 'agent' not in session:
        return redirect('/login_agent')
    return render_template('chat_agent.html')

# API endpoint to send a message (for demo using in-memory list)
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    messages.append({
        'sender': data['role'],
        'text': data['message'],
        'timestamp': datetime.now().strftime("%H:%M:%S")
    })
    return '', 204

# API endpoint to get messages (returns the in-memory message list)
@app.route('/get_messages')
def get_messages():
    return jsonify(messages)

# API endpoint for admin dashboard stats (dummy values)
@app.route('/admin/stats')
def admin_stats():
    return jsonify({
        'agents_online': 3,
        'active_chats': 7,
        'total_users': 154
    })

if __name__ == '__main__':
    app.run(debug=True)
