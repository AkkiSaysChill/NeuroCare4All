from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64
import logging

# To suppress werkzeug's default logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Placeholder for a real focus detection model
def get_focus_score(frame):
    """
    Analyzes a video frame and returns a focus score.
    This is a placeholder function.
    """
    # For now, a dummy score calculation
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # A simple metric: how much of the image is not black
    focus_score = np.mean(gray) / 2.55
    return int(focus_score)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@socketio.on('frame')
def handle_frame(data_image):
    """Handle a new image frame from the client."""
    # Decode the base64 image
    header, encoded = data_image.split(",", 1)
    data = base64.b64decode(encoded)
    nparr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is not None:
        # Get focus score
        score = get_focus_score(frame)
        # Send the score back to the client
        emit('focus_score', {'score': score})

if __name__ == '__main__':
    print("Starting Flask server with SocketIO...")
    print("Navigate to http://127.0.0.1:5000")
    socketio.run(app, debug=True)
