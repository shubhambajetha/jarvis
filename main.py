import eel
import os

from engine.features import *
from engine.coomand import *

def start():
    # Initialize the Eel web app folder
    eel.init('www')

    # eel.start('index.html')

    # Assuming 'sound' is the sound file or identifier you're passing
    playAssetSound('sound_file_or_path_here')

    # Launch Eel with Microsoft Edge in app mode
    eel.start('index.html', mode='edge', host='localhost', block=True)

