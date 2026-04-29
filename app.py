import os
from flask import Flask, request, render_template, redirect, url_for
from models import db, Group, User, Log
from graphs import generate_activity_graph
import telebot

app = Flask(__name__)

# Config MySQL (Defaults to SQLite for local fallback if no MySQL URI is provided)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("MYSQL_URI", "sqlite:///fallback.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    groups_count = Group.query.count()
    logs_count = Log.query.count()
    
    # Generate Matplotlib Graph
    all_logs = Log.query.order_by(Log.timestamp.desc()).limit(100).all()
    generate_activity_graph(all_logs)
    
    return render_template('dashboard.html', groups_count=groups_count, logs_count=logs_count, recent_logs=all_logs[:10])

@app.route('/webhook', methods=['POST'])
def webhook():
    from bot import bot
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '!', 200
    else:
        return "Unsupported Media Type", 415

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
