import pathlib
localPath : pathlib.Path = pathlib.Path(__file__).parent.resolve()

import sys

from math import sqrt, pow
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from ClickableLabel import ClickableLabel
from MicrophoneManager import MicrophoneManager

import pathlib
folderPath = pathlib.Path(__file__).parent.resolve()

def Sign(num):
    return 1 if num >= 0 else -1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.muteManager = MicrophoneManager(self)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.mutedImage = str(folderPath.joinpath("micMuted.png"))
        self.unmutedImage = str(folderPath.joinpath("micUnmuted.png"))
        self.talkingImage = str(folderPath.joinpath("talking.png"))

        self.scale = 1

        self.label = ClickableLabel(self)
        self.SetPixmap(self.unmutedImage)
        curPixMap = QPixmap(self.unmutedImage)
        self.label.setGeometry(0, 0, curPixMap.width(), curPixMap.height())

        self.label.clicked.connect(self.ToggleMute)
        self.muteManager.hearingInputSignal.connect(self.SetTalking)

        self.resize(curPixMap.width(), curPixMap.height())

        self.draggingWindow = False
        self.scalingWindow = False

        self.mutedImageState = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Update)
        self.timer.start(500)

    def Update(self):
        mutedThisFrame = self.muteManager.muted
        self.muteManager.Update()

        if mutedThisFrame != self.mutedImageState:
            self.SetPixmap(self.mutedImage if self.muteManager.muted else self.unmutedImage)
            self.mutedImageState = mutedThisFrame
        pass

    def SetTalking(self, talking):
        if not self.muteManager.muted:
            self.SetPixmap(self.talkingImage if talking else self.unmutedImage)
        pass

    def mousePressEvent(self, a0):
        if (a0.button() == Qt.LeftButton):
            self.draggingWindow = True
        if (a0.button() == Qt.RightButton):
            self.scalingWindow = True

        self.moveStartPos = a0.pos()
        self.lastScale = self.scale
        return super().mousePressEvent(a0)
    
    def mouseMoveEvent(self, a0):
        if self.draggingWindow:
            movement = a0.pos() - self.moveStartPos
            self.move(self.pos() + movement)
        
        elif self.scalingWindow:
            mouseMovedVector = (a0.pos() - self.moveStartPos)
            movementMagnitude = sqrt(mouseMovedVector.x() * mouseMovedVector.x() +\
                                      mouseMovedVector.y() * mouseMovedVector.y()) + 1
            signedMovementMagnitude = movementMagnitude * -Sign(mouseMovedVector.y())
            self.scale = self.lastScale * pow(2, signedMovementMagnitude / 300)

            self.SetScale()

        return super().mouseMoveEvent(a0)
    
    def mouseReleaseEvent(self, a0):
        self.draggingWindow = False
        self.scalingWindow = False
        return super().mouseReleaseEvent(a0)

    def ToggleMute(self):
        self.muteManager.ToggleMute()
        self.SetPixmap(self.mutedImage if self.muteManager.muted else self.unmutedImage)
        pass

    def SetPixmap(self, pixmapName):
        self.currentPixMap = QPixmap(pixmapName)
        self.SetScale()
        pass

    def SetScale(self, scale = -1):
        if scale != -1:
            self.scale = scale

        newSize = QSize(int(self.currentPixMap.width() * self.scale), int(self.currentPixMap.height() * self.scale))
        self.resize(newSize)
        self.label.resize(newSize)
        rescaledImage = QPixmap(self.currentPixMap)
        rescaledImage = rescaledImage.scaled(newSize.width(), newSize.height())
        self.label.setPixmap(rescaledImage)
        pass

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()