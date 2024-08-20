# Self Hosted TikTok Live Stream Overlay

This project is a Flask application that connects to TikTok Live and notifies users of various events such as follows, comments, likes, and when the live stream ends. It uses Flask-SocketIO for real-time communication.

It will currently display the following follower alert, chat messages, likes, stream ending (useless)


## Features

- Connects to TikTok Live using the TikTokLive API.
- Listens for events such as follows, comments, likes, and live stream end.
- Emits notifications to connected clients via WebSocket.
- Saves and loads the TikTok username from a configuration file.

## Requirements

- Python 3.x
- Flask
- Flask-SocketIO
- TikTokLive

## Installation

1. Clone the repository:
   ```bash
   git clone <https://github.com/shibakek2/tiktok-overlay>
   ```

2. Install the required packages:
   ```bash
   pip install flask flask-socketio TikTokLive
   ```

3. Create a `config.json` file in the project directory with the following structure:
   ```json
   {
       "tiktok_username": "@your_username"
   }
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. On the first run, you will be prompted to enter your TikTok username (with `@`). This will be saved in the `config.json` file for future runs.

3. Open your web browser and navigate to `http://localhost:5000` to view the notifications.

## Events

- **FollowEvent**: Notifies when a new follower joins.
- **CommentEvent**: Notifies when a comment is made during the live stream.
- **LikeEvent**: Notifies when a user likes the stream.
- **LiveEndEvent**: Notifies when the live stream ends.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.
