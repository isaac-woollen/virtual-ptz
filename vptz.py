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

        self.pocX = self.alpha
        self.pocY = self.mu

        print(self.alpha, self.mu)

        self.server = Flask(__name__)
        self.socketio = SocketIO(self.server, cors_allowed_origins="*")

        @self.socketio.event
        def connect():
            print("connect")

        @self.socketio.on("info")
        def handle_message(data):
            print(data)
            self.socketio.emit("info", "hello")

        @self.socketio.on("move")
        def handle_move(data):
            if data == "left" and self.pocX > 0:
                self.pocX -= 5
            if data == "right" and self.pocX < self.alpha * 2 - 1:
                self.pocX += 5
            if data == "up" and self.pocY > 0:
                self.pocY -= 5
            if data == "down" and self.pocY < self.mu * 2 - 1:
                self.pocY += 5

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
                    self.pocY : self.pocY + self.capture_height,
                    self.pocX : self.pocX + self.capture_width,
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
