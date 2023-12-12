from ultralytics import YOLO
import time
import numpy as np
import mediapipe as mp


import cv2
from flask import Flask, render_template, request, Response, session, redirect, url_for

from flask_socketio import SocketIO
import yt_dlp as youtube_dl


model_object_detection = YOLO("bisindo.pt")

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')
stop_flag = False

class VideoStreaming(object):
    def __init__(self):
        super(VideoStreaming, self).__init__()
        print ("===== Video Streaming =====")
        self._preview = False
        self._flipH = False
        self._detect = False
        self._model = False
        self._confidence = 75.0
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

    @property
    def confidence(self):
        return self._confidence

    @confidence.setter
    def confidence(self, value):
        self._confidence = int(value)

    @property
    def preview(self):
        return self._preview

    @preview.setter
    def preview(self, value):
        self._preview = bool(value)

    @property
    def flipH(self):
        return self._flipH

    @flipH.setter
    def flipH(self, value):
        self._flipH = bool(value)

    @property
    def detect(self):
        return self._detect

    @detect.setter
    def detect(self, value):
        self._detect = bool(value)


    def show(self, url):
        print(url)
        self._preview = False
        self._flipH = False
        self._detect = False

        self._confidence = 75.0
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "best",
            "forceurl": True,
        }

        if url == '0':
            cap = cv2.VideoCapture(0)
        else:
            
            ydl = youtube_dl.YoutubeDL(ydl_opts)

            # Extract the video URL
            info = ydl.extract_info(url, download=False)
            url = info["url"]

            cap = cv2.VideoCapture(url)

        while True:
            if self._preview:
                if stop_flag:
                    print("Process Stopped")
                    return

                grabbed, frame = cap.read()
                if not grabbed:
                    break
                if self.flipH:
                    frame = cv2.flip(frame, 1)
                # if self.detect:
                #     print(self._confidence)

                #     # frame = cv2.cvtColor(snap, cv2.COLOR_BGR2RGB)
                #     # frame = cv2.resize(frame, (500,500
                #     # ))
                #     # Detect objects
                #     results = model_object_detection.predict(frame, conf=self._confidence/100)

                #     frame, labels = results[0].plot()
                #     list_labels = []
                #     # labels_confidences
                #     for label in labels:
                #         confidence = label.split(" ")[-1]
                #         label = (label.split(" "))[:-1]
                #         label = " ".join(label)
                #         list_labels.append(label)
                #         list_labels.append(confidence)
                #         socketio.emit('label', list_labels)
                # # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                # frame = cv2.imencode(".jpg", frame)[1].tobytes()
                # yield (b'--frame\r\n'
                #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                if self.detect:
                    frame_yolo = frame.copy()
                    results_yolo = model_object_detection.predict(frame_yolo, conf=self._confidence / 100)

                    frame_yolo, labels = results_yolo[0].plot()
                    list_labels = []
                    # labels_confidences
                    for label in labels:
                        confidence = label.split(" ")[-1]
                        label = (label.split(" "))[:-1]
                        label = " ".join(label)
                        list_labels.append(label)
                        list_labels.append(confidence)
                        socketio.emit('label', list_labels)

                    # Convert the image to RGB for processing with MediaPipe
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.hands.process(image)
                    
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp.solutions.drawing_utils.draw_landmarks(
                                frame,
                                hand_landmarks,
                                self.mp_hands.HAND_CONNECTIONS,
                                landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=4, circle_radius=3),
                                connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2), 
                            )


                frame = cv2.imencode(".jpg", frame)[1].tobytes()
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
                )
            else:
                snap = np.zeros((
                    1000,
                    1000
                ), np.uint8)
                label = "Streaming Off"
                H, W = snap.shape
                font = cv2.FONT_HERSHEY_PLAIN
                color = (255, 255, 255)
                cv2.putText(snap, label, (W//2 - 100, H//2),
                            font, 2, color, 2)
                frame = cv2.imencode(".jpg", snap)[1].tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# check_settings()
VIDEO = VideoStreaming()


@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('hompage.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    print("index")
    global stop_flag
    stop_flag = False
    if request.method == 'POST':
        print("Index post request")
        url = request.form['url']
        print("index: ", url)
        session['url'] = url
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    url = session.get('url', None)
    print("video feed: ", url)
    if url is None:
        return redirect(url_for('homepage'))

    return Response(VIDEO.show(url), mimetype='multipart/x-mixed-replace; boundary=frame')

# * Button requests
@app.route("/request_preview_switch")
def request_preview_switch():
    VIDEO.preview = not VIDEO.preview
    print("*"*10, VIDEO.preview)
    return "nothing"

@app.route("/request_flipH_switch")
def request_flipH_switch():
    VIDEO.flipH = not VIDEO.flipH
    print("*"*10, VIDEO.flipH)
    return "nothing"

@app.route("/request_run_model_switch")
def request_run_model_switch():
    VIDEO.detect = not VIDEO.detect
    print("*"*10, VIDEO.detect)
    return "nothing"


@app.route('/update_slider_value', methods=['POST'])
def update_slider_value():
    slider_value = request.form['sliderValue']
    VIDEO.confidence = slider_value
    return 'OK'

@app.route('/stop_process')
def stop_process():
    print("Process stop Request")
    global stop_flag
    stop_flag = True
    return 'Process Stop Request'

@socketio.on('connect')
def test_connect():
    print('Connected')

if __name__ == "__main__":
    socketio.run(app, debug=True)
