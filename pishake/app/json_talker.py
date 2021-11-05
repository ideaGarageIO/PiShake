import zmq
import random
import sys
import time
import json

class Client():
    def __init__(self, port="5557", ip="127.0.0.1"):
        self.port = port
        self.ip = ip
        self.url = "tcp://{}:{}".format(self.ip, self.port)
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self.frequency = 60
        self.duration = 30
        self.gain = 1
        self.loops = 1


    def set_gain(self, gain):
        self.gain = gain
        self.build_message()


    def build_message(self):
        cmd_dict


    def send_msg(self, msg):
        try:
            self._socket.bind(self.url)
            self._socket.send(msg)

        except Exception as e:
            print("Error {}".format(e))

        finally:
            self._socket.unbind(self.url)


port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)
# Example of a decorator in which
# we pass in an object and perform
# actions on the object.

def sendmsg(client):
    action = input("action:")
    frequency = input("frequency:")
    duration = input("duration:")
    gain = input("gain:")
    loops = input("loops:")
    cmd_dict = {'action': action,'frequency':frequency, 'duration':duration, 'gain':gain, 'loops':loops}
    cmd_dict = json.dumps(cmd_dict)
    loaded_json = json.loads(cmd_dict)
    print("Sending: Frequency: {} Duration: {}".format(frequency, duration))
    client.send_json(loaded_json)
    succ = client.recv_string()
    if succ:
        print("Transaction complete")

try:
    while True:
        sendmsg(socket)

finally:
    socket.close()
