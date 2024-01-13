import random
from PySide6 import QtCore, QtWidgets


class MainWindow(QtWidgets.QWidget):
    """
    Handles state and interaction with the main window of the app
    """
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):  # pylint: disable=missing-function-docstring
        self.text.setText(random.choice(self.hello))
