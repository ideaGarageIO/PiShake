"""
Webserver interface
"""

from flask import Flask
from flask import render_template
from flask import request
import socket
import subprocess
from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play
import zmq
import time
import json
app = Flask(__name__)

#POST request == Store data on Webserver
#GET request = Send data to brows

version = "0.0.1"
frequency = 60
duration = 50
gain = 1
loops = 1
host = "127.0.0.1"
playerPort = '5557'
playerURL = 'tcp://{}:{}'.format(host, playerPort)
context = zmq.Context()
socket = context.socket(zmq.PUB)


@app.route('/')
def splash():
    playTone = True
    input_signal = request.args.get("signal")
    if not input_signal:
        input_signal = 'sine'
        playTone = False
    else:
        update_signal(input_signal)
    input_frequency = request.args.get("frequency")
    if not input_frequency:
        input_frequency = 0
        playTone = False
    else:
        update_frequency(int(input_frequency))
    input_duration = request.args.get("duration")
    if not input_duration:
        input_duration = 0
        plalyTone = False
    else:
        update_duration(int(input_duration))
    input_gain = request.args.get("gain")
    if not input_gain:
        input_gain = 1
    else:
        update_gain(input_gain)
    input_loops = request.args.get("loops")
    if not input_loops:
        input_loops = 1
    else:
        update_loops(input_loops)
    if playTone:
        #sendmsg(frequency=frequency, duration=duration)
        play_tone(signal=signal, frequency=frequency, duration = duration,
                  gain=gain, loops=loops)
    return render_template("splash.html", frequency=frequency,
                           duration=duration, gain=gain, loops=loops)

@app.route('/stop')
def stop(): 
    try:
        connection = socket.bind(playerURL)
        time.sleep(0.5)
        cmd_dict = {'action':'stop', 'frequency':0, 'duration':0,
                    'gain':0, 'loops':0}
        cmd_dict = json.dumps(cmd_dict)
        loaded_json = json.loads(cmd_dict)
        socket.send_json(loaded_json)
    except Exception as e:
        print("Error {}".format(e))
    finally:
        connection = socket.unbind(playerURL)

    return render_template("splash.html", frequency=frequency,
                           duration=duration, gain=gain, loops=loops)

@app.route('/config')
def config():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = (s.getsockname()[0])
    s.close()
    return render_template("config.html", ip_address=ip_address)


@app.route('/upload', methods=['POST'])
def upload():
    return "Upload"


@app.route('/about')
def about():
    return render_template("about.html", version=version)

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/test_bad_data')
def test_bad_data():
    try:
        connection = socket.bind(playerURL)
        time.sleep(0.5)
        cmd = "bad data"
        cmd = json.dumps(cmd)
        loaded_json = json.loads(cmd)
        socket.send_json(loaded_json)
    except Exception as e:
        print("Error {}".format(e))
    finally:
        connection = socket.unbind(playerURL)

    return render_template("test.html")


def play_tone(signal='sine',frequency=60, duration=30, gain=1, loops=1):
    """
    Simple function responsible for playing a toneself.

    Inputs: frequency (Hz)
            duration (seconds)

    Ouputs: Played tone

    """
    sendmsg(signal,frequency, duration, gain, loops)


def update_signal(signal_update):
    global signal
    signal = signal_update


def update_frequency(freq_update):
    global frequency
    frequency = freq_update


def update_duration(dur_update):
    global duration
    duration = dur_update


def update_gain(gain_update):
    global gain
    gain = gain_update


def update_loops(loops_update):
    global loops
    loops = loops_update


def sendmsg(signal, frequency, duration, gain, loops):
    print("sending message")
    try:
        connection = socket.bind(playerURL)
        time.sleep(0.5)
        cmd_dict = {'action':'play', 'signal':signal, 'frequency':frequency, 'duration':duration,
                    'gain':gain, 'loops':loops}
        cmd_dict = json.dumps(cmd_dict)
        loaded_json = json.loads(cmd_dict)
        socket.send_json(loaded_json)
    except Exception as e:
        print("Error {}".format(e))
    finally:
        connection = socket.unbind(playerURL)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000, debug=True)
