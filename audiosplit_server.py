from flask import Flask
from pynput.keyboard import Key, Controller

keyboard = Controller()
key = '['
app = Flask(__name__)

@app.route("/")
def hello_world():
    print("Received something!!")
    keyboard.press(key)
    keyboard.release(key)
    return "Split request received!"
