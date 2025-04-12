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

# In-memory messages list for live view demo (for production, use the messages table exclusively)
messages = []

# Home page
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

# Superadmin Dashboard
@app.route('/dashboard_admin')
def dashboard_admin():
    if 'admin' not in session:
        return redirect('/login_admin')
    return render_template('dashboard_admin.html')

# Create Agent (admin functionality)
@app.route('/create_agent', methods=['GET', 'POST'])
def create_agent():
    if 'admin' not in session:
        return redirect('/login_admin')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM agents WHERE username=%s", (username,))
        existing = cursor.fetchone()
        if existing:
            return "Agent username already exists. Choose another.", 400
        cursor.execute("INSERT INTO agents (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        return redirect('/dashboard_admin')
    
    return render_template('create_agent.html')

# User Chat Page (no login required)
@app.route('/chat_user')
def chat_user():
    return render_template('chat_user.html')

# Agent Chat Page (login required)
@app.route('/chat_agent')
def chat_agent():
    if 'agent' not in session:
        return redirect('/login_agent')
    return render_template('chat_agent.html')

# API endpoint to send a message
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    role = data.get('role')
    message_content = data.get('message')
    
    # Use actual agent name from session if the sender is an agent
    sender = role
    if role == 'agent':
        sender = session.get('agent', 'agent')
    
    # For demonstration, if a user sends a message, we assign it to a default agent (could be improved with proper pairing)
    if role == 'user':
        receiver = "agent1"  # Replace with actual agent assignment logic if available
    elif role == 'agent':
        receiver = "user"
    else:
        receiver = ""
    
    timestamp = datetime.now()
    
    # Insert into MySQL messages table
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO messages (sender, receiver, content, timestamp) VALUES (%s, %s, %s, %s)", 
                   (sender, receiver, message_content, timestamp))
    mysql.connection.commit()
    
    # Also add to in-memory list for live updates in the demo
    messages.append({
        'sender': sender,
        'text': message_content,
        'timestamp': timestamp.strftime("%H:%M:%S")
    })
    return '', 204

# API endpoint to get messages
@app.route('/get_messages')
def get_messages():
    return jsonify(messages)

# API endpoint for admin stats (dummy values for now)
@app.route('/admin/stats')
def admin_stats():
    return jsonify({
        'agents_online': 3,
        'active_chats': 7,
        'total_users': 154
    })

# API endpoint to provide chart data grouped by agent name
@app.route('/admin/chart_data')
def admin_chart_data():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Count messages sent by agents (using the agent name stored in sender)
    cursor.execute("SELECT sender as agent, COUNT(*) as chat_count FROM messages WHERE sender != 'user' GROUP BY sender")
    data = cursor.fetchall()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
