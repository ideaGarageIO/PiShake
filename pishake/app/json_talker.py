from logging import raiseExceptions
import zmq
import random
import sys
import time
import json
import socket

class Client():
    def __init__(self, port="5557", ip="127.0.0.1"):
        self.port = port
        self.ip = ip
        self.serverURL = "tcp://{}:{}".format(self.ip, self.port)
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self.connection = None
        self.frequency = 60
        self.duration = 30
        self.gain = 1
        self.loops = 1


    def connect(self):
        # This is a client object which performs a connection
        print("Connecting to {}:{}".format(self.ip, self.port))
        self.connection = self._socket.connect(self.serverURL)
        assert(self.connection != None)

    def set_gain(self, gain):
        if(gain<=0):
            print("Invalid gain")
            raise Exception("Invalid gain")
        else:
            print("Setting gain: {}".format(gain))
            self.gain = gain

    def set_duration(self, duration):
        if duration <=0:
            print("Invalid duration")
            raise Exception("Invalid duration")
        else:
            print("Setting duration: {}".format(duration))
            self.duration = duration

    def set_frequency(self, frequency):
        if(frequency<0):
            print("Invalid frequency")
            raise Exception("Invalid Frequecy")
        else:
            print("Setting frequency: {}".format(frequency))
            self.frequency = frequency


    def send_msg(self, signal, frequency, duration, gain, loops):
        print("Sending message")
        try:
            self._socket.connect(self.serverURL)
            time.sleep(0.5)
            cmd_dict = {"action":"play", 
                        "signal":signal,
                        "duration":duration, 
                        "frequency":frequency, 
                        "gain":gain,
                        "loops":loops}
            cmd_dict = json.dumps(cmd_dict)
            loaded_json = json.loads(cmd_dict)
            self._socket.send_json(loaded_json)
            reciept = self._socket.recv()

        except Exception as e:
            print("Error {}".format(e))

        finally:
            self._socket.disconnect(self.serverURL)

    def run_sine_sweeps(self, start_frequency=100, end_frequency=500, increment=25):
        for freq in range(start_frequency, end_frequency, increment):
            self.set_frequency(freq)
            self.set_duration(10)
            self.send_msg("sine", self.frequency, self.duration, self.gain, self.loops)
            time.sleep(self.duration+3)

if __name__ == "__main__":
    client = Client()
    client.run_sine_sweeps()