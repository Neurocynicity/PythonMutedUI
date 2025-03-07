from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel


class ClickableLabel(QLabel):
    pressPos = None
    clicked = pyqtSignal()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressPos = event.pos()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if (self.pressPos is not None and \
            event.button() == Qt.LeftButton and \
            event.pos() in self.rect()):
            # (event.pos() - self.pressPos)'s magnitude is higher than like 20,20):
                self.clicked.emit()
        self.pressPos = None
        return super().mouseReleaseEvent(event)
