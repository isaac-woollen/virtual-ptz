import cv2
from threading import Thread
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import json


class VPTZ:
    def __init__(self, src=0, port=7777):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

        self.width = int(self.stream.get(3))
        self.height = int(self.stream.get(4))

        self.capture_width = 640
        self.capture_height = 360

        # Helps us keep track on where to start grabbing pixels from capture array
        self.alpha = int((self.width - self.capture_width) / 2)
        self.mu = int((self.height - self.capture_height) / 2)

        print(self.alpha, self.mu)

        self.server = Flask(__name__)
        self.socketio = SocketIO(self.server, cors_allowed_origins="*")

        @self.socketio.on("message")
        def handle_message(data):
            print(data)
            self.socketio.emit("response", str(self.width) + str(self.height))

        @self.socketio.on("move")
        def handle_move(data):
            if data == "left" and self.alpha > 0:
                self.alpha -= 5
            if data == "right" and self.alpha > 0:
                self.alpha += 5

    def start_camera(self):
        Thread(target=self.get_video, args=()).start()
        return self

    def start_server(self):
        self.socketio.run(self.server)
        return self

    def get_video(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                self.frame = self.frame[
                    self.mu : self.mu + self.capture_height,
                    self.alpha : self.alpha + self.capture_width,
                ]


if __name__ == "__main__":
    vptz_obj = VPTZ()
    vptz_obj.start_camera()
    server_thread = Thread(target=vptz_obj.start_server, args=())
    server_thread.daemon = True
    server_thread.start()

    while True:
        if (cv2.waitKey(1) == ord("q")) or vptz_obj.stopped:
            vptz_obj.stopped = True
            break

        frame = vptz_obj.frame
        cv2.imshow("frame", frame)
