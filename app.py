from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64
import logging
import time


# To suppress werkzeug's default logging
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config["SECRET_KEY"] = "A_shit_here_we_go_again"
socketio = SocketIO(app)

# Load the pre-trained Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def get_focus_score(frame):
    """
    Analyzes a video frame and returns a focus score based on face detection.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # TODO: add functionality to identify distracted face...

    if len(faces) > 0:
        return 100  # Face detected
    else:
        return 0  # No face detected


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


last_face_time = time.time()
alarm_on = False


@socketio.on("frame")
def handle_frame(data_image):
    """Handle a new image frame from the client."""
    global last_face_time, alarm_on

    # Decode the base64 image
    header, encoded = data_image.split(",", 1)
    data = base64.b64decode(encoded)
    nparr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is not None:
        # Get focus score
        score = get_focus_score(frame)

        if score > 0:
            last_face_time = time.time()
            alarm_on = False
        else:
            if not alarm_on and time.time() - last_face_time > 3:
                emit("alarm")
                alarm_on = True

        # Send the score back to the client
        emit("focus_score", {"score": score})


if __name__ == "__main__":
    print("Starting Flask server with SocketIO...")
    print("Navigate to http://127.0.0.1:5000")
    socketio.run(app, debug=True)

