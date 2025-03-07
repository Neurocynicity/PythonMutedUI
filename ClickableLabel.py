from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel
from math import sqrt


class ClickableLabel(QLabel):
    pressPos = None
    clicked = pyqtSignal()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressPos = event.globalPos()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.pressPos is None or \
             event.button() != Qt.LeftButton:
            return super().mouseReleaseEvent(event)

        mouseMoveVect = event.globalPos() - self.pressPos
        mouseMoveDistance = sqrt(mouseMoveVect.x() * mouseMoveVect.x() + mouseMoveVect.y() * mouseMoveVect.y())

        if mouseMoveDistance < 30:
                self.clicked.emit()
        self.pressPos = None
        return super().mouseReleaseEvent(event)
        
