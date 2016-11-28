import MainWindow
import os
import sys

def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command',
                             'ValidatorDB',
                             label='ValidatorDB',
                             command=lambda s=self: MainWindow.MAINWINDOW)
path = os.path.dirname(MainWindow)
sys.path.append(path)