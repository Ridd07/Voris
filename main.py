import os
import eel

from engine.features import *
from engine.command import *

def start():
    eel.init("www")

    playAssistantSound()

    os.system('start msedge.exe --app="http://localhost:8888/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True, port=8888)