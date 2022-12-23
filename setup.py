from distutils.core import setup # Need this to handle modules
import py2exe
import PyQt6.sip
import sys, pickle, shutil, math
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QPushButton, QLabel, QHBoxLayout, \
    QVBoxLayout, QComboBox, QLineEdit, QSlider, QSpacerItem, QMessageBox
from PyQt6.QtGui import QFont
from addition import *
from Type205 import *
from PyQt6.QtCore import Qt

opts = {'py2exe': {"includes" : ["PyQt6.sip"]}}

setup(console=['pyqt.py'], options= opts)