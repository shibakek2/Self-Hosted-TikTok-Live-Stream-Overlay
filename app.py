from flask import Flask, render_template
from flask_socketio import SocketIO
from TikTokLive import TikTokLiveClient
from TikTokLive.events import FollowEvent, CommentEvent, LikeEvent, ConnectEvent, LiveEndEvent
import threading
import json 
import sys
import os

def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config.get('tiktok_username', None)
    except FileNotFoundError:
        return None

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_config(username):
    with open('config.json', 'w') as f:
        json.dump({'tiktok_username': username}, f)

tiktok_username = load_config()
if not tiktok_username:
    clear_terminal()
    print("First time startup")
    tiktok_username = input("Please enter your TikTok username (with @): ")
    save_config(tiktok_username)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')  # Specify async_mode
try:
    client = TikTokLiveClient(tiktok_username)
    print("Successfully connected to TikTok Live.")
except Exception as e:
    print("Failed to connect to TikTok Live.")
    print(f"Error: {e}")
    sys.exit(1)

@client.on(LiveEndEvent)
async def on_live_end(_):
    print("The stream has ended")
    socketio.emit('live_end_event', {'message': 'The stream has ended'})

@client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    print(event.user.unique_id)
    socketio.emit('follow_event', {'message': f'Thank you for the follow {event.user.unique_id}'})

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    socketio.emit('comment_event', {'message': f'{event.user.unique_id}: {event.comment}'})

@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    socketio.emit('like_event', {'message': f'{event.user.unique_id} liked the stream!'})
    
@app.route('/')
def index():
    return render_template('alerts.html')

def run_client():
    try:
        client.run()
    except Exception as e:
        clear_terminal()
        print("Please make sure you are live before running the program and that your username is correct.")
        print(f"Error: {e}")
        answer = input("Do you want to try again? (y/n): ") 
        if answer.lower() == 'y':
            run_client()
        else:
            sys.exit(1)

def run_app():
    socketio.run(app, debug=True, use_reloader=False, port=5000)
if __name__ == '__main__':
    clear_terminal()
    client_thread = threading.Thread(target=run_client)
    app_thread = threading.Thread(target=run_app)
    client_thread.start()
    app_thread.start()
    client_thread.join()
    app_thread.join()