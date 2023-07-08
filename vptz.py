import cv2
from threading import Thread
from flask import Flask
from flask_socketio import SocketIO
import json
import pyvirtualcam
from engineio.async_drivers import gevent
import numpy

directions = ["left", "right", "up", "down"]

import socket


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("192.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP

def set_client_config(ip, port):
    config_init = {
        "vptz-ip" : ip,
        "vptz-port": port
    }

    config = json.dumps(config_init, indent=4)

    with open("client/server/config.json", "w") as outfile:
        outfile.write(config)
        outfile.close()
    

class VPTZ:
    def __init__(self, src=0, port=7777):

        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

        self.port = port
        set_client_config(get_local_ip(), port)

        self.width = int(self.stream.get(3))
        self.height = int(self.stream.get(4))

        self.last_action = ""

        self.capture_width = 1280
        self.capture_height = 720

        # Helps us keep track on where to start grabbing pixels from capture array
        self.alpha = int((self.width - self.capture_width) / 2)
        self.mu = int((self.height - self.capture_height) / 2)

        self.pocX = self.alpha
        self.pocY = self.mu

        self.speed_array = [0, 0]  # Horizontal, vertical

        self.timing_index = -1

        self.server = Flask(__name__)
        self.socketio = SocketIO(self.server, cors_allowed_origins="*")

        @self.socketio.on("info")
        def handle_message(data):
            status = {
                "xPOS": "%.2f" % ((self.pocX - self.alpha) / self.alpha * 100),
                "yPOS": "%.2f" % ((self.pocY - self.mu) / self.mu * -100),
                "xSpeed": str(abs(self.speed_array[0])),
                "ySpeed": str(abs(self.speed_array[1])),
            }

            status = json.dumps(status)
            self.socketio.emit("info", status)

        @self.socketio.on("action")
        def handle_move(data):
            self.last_action = data

            if data == "left":
                if self.speed_array[0] - 4 < -20:
                    self.speed_array[0] = -20
                else:
                    self.speed_array[0] -= 4

            if data == "right":
                if self.speed_array[0] + 4 > 20:
                    self.speed_array[0] = 20
                else:
                    self.speed_array[0] += 4

            if data == "up":
                if self.speed_array[1] - 4 < -20:
                    self.speed_array[1] = -20
                else:
                    self.speed_array[1] -= 4

            if data == "down":
                if self.speed_array[1] + 4 > 20:
                    self.speed_array[1] = 20
                else:
                    self.speed_array[1] += 4

            self.socketio.emit("action", self.last_action)

    def start_camera(self):
        Thread(target=self.get_video, args=()).start()
        return self

    def start_server(self):
        self.socketio.run(self.server, port=self.port, host=get_local_ip())
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

                if self.speed_array[0] + self.pocX < 0:
                    self.pocX = 0
                elif self.speed_array[0] + self.pocX > self.alpha * 2:
                    self.pocX = self.alpha * 2
                else:
                    self.pocX += self.speed_array[0]

                if self.speed_array[1] + self.pocY < 0:
                    self.pocY = 0
                elif self.speed_array[1] + self.pocY > self.mu * 2:
                    self.pocY = self.mu * 2
                else:
                    self.pocY += self.speed_array[1]

                for i in range(len(self.speed_array)):
                    if self.speed_array[i] > 0:
                        self.speed_array[i] -= 1
                    elif self.speed_array[i] < 0:
                        self.speed_array[i] += 1


if __name__ == "__main__":
    vptz_obj = VPTZ()
    vptz_obj.start_camera()
    server_thread = Thread(target=vptz_obj.start_server, args=())
    server_thread.daemon = True
    server_thread.start()

    fmt = pyvirtualcam.PixelFormat.BGR

    with pyvirtualcam.Camera(
        width=vptz_obj.capture_width, height=vptz_obj.capture_height, fps=30, fmt=fmt
    ) as cam:
        while True:
            frame = vptz_obj.frame

            frame = cv2.resize(
                frame,
                (vptz_obj.capture_width, vptz_obj.capture_height),
                interpolation=cv2.BORDER_DEFAULT,
            )
            # cv2.imshow('my webcam', frame)
            cam.send(frame)
            cam.sleep_until_next_frame()
            if cv2.waitKey(1) == 27:
                break  # esc to quit
        cv2.destroyAllWindows()
