import telebot
import os
from models import db, Group, User, Log
from nlp import NLPModeration

bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "DUMMY_TOKEN")
bot = telebot.TeleBot(bot_token)

def get_app_context():
    from app import app
    return app.app_context()

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.chat.type == "private":
        return

    with get_app_context():
        # Upsert Group
        group = Group.query.filter_by(group_id=message.chat.id).first()
        if not group:
            group = Group(group_id=message.chat.id, title=message.chat.title)
            db.session.add(group)
            db.session.commit()
            
        # Analysis (Includes NLP and NER)
        analysis = NLPModeration.analyze_message(message.text)
        
        should_delete = False
        reason = ""
        
        if analysis["is_spam"] and group.anti_spam:
            should_delete = True
            reason = "Spam Link Detected"
        elif analysis["is_toxic"] and group.anti_toxicity:
            should_delete = True
            reason = f"Toxic Content (Entities found: {[e['text'] for e in analysis['entities']]})"
            
        if should_delete:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                
                user = User.query.filter_by(user_id=message.from_user.id, group_id=message.chat.id).first()
                if not user:
                    user = User(user_id=message.from_user.id, group_id=message.chat.id, first_name=message.from_user.first_name)
                    db.session.add(user)
                    
                user.warnings += 1
                
                log = Log(group_id=message.chat.id, action="deleted", reason=reason, target_user_id=message.from_user.id)
                db.session.add(log)
                db.session.commit()
                
                bot.send_message(message.chat.id, f"@{message.from_user.username or message.from_user.first_name}, message deleted. Reason: {reason}. Warning {user.warnings}/{group.max_warnings}")
                
                if user.warnings >= group.max_warnings:
                    bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False)
                    bot.send_message(message.chat.id, f"User muted for reaching max warnings.")
                    db.session.add(Log(group_id=message.chat.id, action="muted", reason="Max warnings", target_user_id=message.from_user.id))
                    db.session.commit()
            except Exception as e:
                print("Error deleting:", e)

def set_webhook(url):
    bot.remove_webhook()
    bot.set_webhook(url=url)
