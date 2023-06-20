import cv2
from threading import Thread
from flask import Flask, jsonify, request
import json


class VPTZ:
    def __init__(self, src=0, port=7777):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

        self.width = int(self.stream.get(3))
        self.height = int(self.stream.get(4))

        self.server = Flask(__name__)
        self.init_server_routes()

    def start_camera(self):
        Thread(target=self.get_video, args=()).start()
        return self

    def start_server(self):
        Thread(target=self.server.run(), args=()).start()

    def init_server_routes(self):
        @self.server.route("/", methods=["GET"])
        def index():
            return "<h1>vPTZ Message Server</h1>"

        @self.server.route("/info", methods=["GET"])
        def info():
            print(f"Info has been requested from: {request.remote_addr} via /info")
            return f"Info: {str(self.stream.get(3))}, {str(self.stream.get(4))}\n"

    def get_video(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                self.frame = self.frame[
                    9 * 30 : self.height - 9 * 30, 16 * 30 : self.width - 16 * 30
                ]


if __name__ == "__main__":
    vptz_obj = VPTZ()
    vptz_obj.start_camera()
    vptz_obj.start_server()

    while True:
        if (cv2.waitKey(1) == ord("q")) or vptz_obj.stopped:
            vptz_obj.stopped = True
            break

        frame = vptz_obj.frame
        cv2.imshow("frame", frame)
