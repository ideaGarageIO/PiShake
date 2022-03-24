import zmq
import random
import time
import sys
import json
from pydub import AudioSegment
from pydub.generators import Sine, Sawtooth,Pulse, Square, Triangle, Pulse, WhiteNoise
from pydub.playback import play
import simpleaudio as sa

class FrequencyGenerator():
    """
    Player class that manages putting generated tones into the play buffer.
    """
    def __init__(self, port="5557", ip="127.0.0.1"):
        self.port = port
        self.ip = ip
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        # This is a server object which binds the connection
        self._socket.bind("tcp://*:{}".format(port))
        self._play_obj = None
        self.frequency = 60
        self.duration = 30
        self.gain = 1
        self.loops = 1
        self.supported_types = ['triangle', 'sine', 'square', 'sawtooth', 'pulse', 'whitenoise']


    def recieve_message_test(self):
        """
        Method for testing message handling
        """


    def recieve_message(self):
        """
        Method responsible for checking input msg and passing information to start/stop a play buffer.
        """
        print('Listening on tcp://{}:{}'.format(self.ip, self.port))
        while True:
            msg = self._socket.recv()
            msg = msg.decode('utf-8')
            try:
                msg = json.loads(msg)
                self._socket.send(b"Message Recieved")
            except ValueError:
                msg = str(msg)
                print("Error occurred with: {}".format(msg))
            if isinstance(msg, dict):
                if msg['action'] == 'play':
                    signal = msg['signal']
                    if signal not in self.supported_types:
                        print("Signal: {} not supported".format(signal))
                    else:
                        frequency = int(msg['frequency'])
                        duration = float(msg['duration'])
                        gain = float(msg['gain'])
                        loops = int(msg['loops'])
                        self.generate_signal(signal, frequency, duration*10, gain, loops)

                if msg['action'] == 'stop':
                    print("Recieved action: {}".format(msg['action']))
                    self.stop()
            else:
                raise Exception("Malformed command")
                
    def stop(self):
        """
        Method responsible for stopping the play buffer and terminating tone during playback
        """
        if self._play_obj:
            print("Stopping buffer")
            self._play_obj.stop()


    def generate_signal(self, signal, frequency, duration, gain, loops):
        """
        Method responsible for generating signal and adding it to the playh buffer.
        """
        tone = None
        print("Generating {} signal".format(signal.lower()))
        if signal.lower() == "square":
            tone = Square(frequency).to_audio_segment(duration*100)
        elif signal.lower() == "pulse":
            tone = Pulse(frequency).to_audio_segment(duration*100)
        elif signal.lower() == "sawtooth":
            tone = Sawtooth(frequency).to_audio_segment(duration*100)
        elif signal.lower() == "whitenoise":
            tone = WhiteNoise().to_audio_segment(duration*100)
        else:
            tone = Sine(frequency).to_audio_segment(duration*100)
        if tone != None:
            print("Tone = {} generated".format(signal.capitalize()))
        else:
            print("Failed to generate {} signal".format(signal.capitalize()))
        print("Playing Type: {}, Freuqncy: {}, Duration: {}, Gain: {}, Loops: {}".format(signal.capitalize(),
                                                                                         frequency, 
                                                                                         duration/10,
                                                                                         gain,
                                                                                         loops))
        if tone:
            self._play_obj = sa.play_buffer(tone.raw_data, 
                                            num_channels = tone.channels, 
                                            bytes_per_sample = tone.sample_width,
                                            sample_rate = tone.frame_rate)

        

if __name__ == "__main__":
    server = FrequencyGenerator()
    server.recieve_message()
