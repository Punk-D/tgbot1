import telebot
import threading
import time

TOKEN = '7740897731:AAFFUn3XLSdC--SdbrNos3DLMZsEaKHe5WU'

bot = telebot.TeleBot(TOKEN)

STUDY_DURATION = 25 * 60  
BREAK_DURATION = 5 * 60   

user_sessions = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "Welcome to Study Buddy Bot! Use /startstudy to begin a session."
    )

@bot.message_handler(commands=['startstudy'])
def start_study(message):
    user_id = message.chat.id
    
    if user_id in user_sessions and user_sessions[user_id]['active']:
        bot.send_message(user_id, "You're already in a study session!")
        return
    
    bot.send_message(user_id, "Starting a study session! Focus for 25 minutes.")
    user_sessions[user_id] = {
        'active': True,
        'phase': 'study',
        'remaining_time': STUDY_DURATION,
        'paused': False,
        'thread': None
    }
    
    study_thread = threading.Thread(target=study_timer, args=(user_id,))
    study_thread.start()
    user_sessions[user_id]['thread'] = study_thread

def study_timer(user_id):
    session = user_sessions[user_id]
    
    while session['remaining_time'] > 0:
        if session['paused']:
            time.sleep(1) 
            continue
        
        time.sleep(1)
        session['remaining_time'] -= 1

    if session['phase'] == 'study' and not session['paused']:
        bot.send_message(user_id, "Study time is over! Take a 5-minute break.")
        session['phase'] = 'break'
        session['remaining_time'] = BREAK_DURATION
        study_timer(user_id) 
    elif session['phase'] == 'break' and not session['paused']:
        bot.send_message(user_id, "Break time is over! Ready to start another session? Use /startstudy.")
        session['active'] = False

@bot.message_handler(commands=['pausestudy'])
def pause_study(message):
    user_id = message.chat.id
    if user_id in user_sessions and user_sessions[user_id]['active']:
        session = user_sessions[user_id]
        if session['paused']:
            bot.send_message(user_id, "The session is already paused!")
        else:
            session['paused'] = True
            bot.send_message(user_id, "The study session is now paused. Use /resumestudy to continue.")
    else:
        bot.send_message(user_id, "You don't have an active session to pause!")

@bot.message_handler(commands=['resumestudy'])
def resume_study(message):
    user_id = message.chat.id
    if user_id in user_sessions and user_sessions[user_id]['active']:
        session = user_sessions[user_id]
        if session['paused']:
            session['paused'] = False
            bot.send_message(user_id, "Resuming your session!")
        else:
            bot.send_message(user_id, "Your session is already running!")
    else:
        bot.send_message(user_id, "You don't have a paused session to resume!")

@bot.message_handler(func=lambda message: True)
def fallback_response(message):
    bot.send_message(message.chat.id, "I'm sorry, I don't understand that command. Use /startstudy to begin!")


bot.polling()
