"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
from threading import Thread

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


def print_volume_handler(unused_addr, args, volume):
    print("[{0}] ~ {1}".format(args[0], volume))


def print_compute_handler(unused_addr, args, volume, v2):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError:
        pass


def print_info(unused_addr):
    print("This is info")


class CommServer:
    def __init__(self, port):
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/info", self.print_info, needs_reply_address=True)

        self.server = osc_server.ThreadingOSCUDPServer(
            ("127.0.0.1", port), self.dispatcher
        )

    def start(self):
        Thread(target=self.server.serve_forever, args=()).start()
        return self

    def print_info(self, addr, addr1):
        print("Info has been requested from:", addr, addr1)


if __name__ == "__main__":
    comm_server = CommServer(6738)
    comm_server.start()

    print("Hello")
