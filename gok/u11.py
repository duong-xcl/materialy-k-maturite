from PyQt5 import QtWidgets
import random

app = QtWidgets.QApplication([])

hlavni_okno = QtWidgets.QWidget()
hlavni_okno.setWindowTitle("trololo")

usporadani = QtWidgets.QHBoxLayout()
hlavni_okno.setLayout(usporadani)

napis = QtWidgets.QLabel("Don't touch")
usporadani.addWidget(napis)

tlacitko = QtWidgets.QPushButton("Touch pls")
usporadani.addWidget(tlacitko)

def zmen_text():
    novyText = ["NOO","WHYY","FUCK YOUUU"]
    napis.setText(random.choice(novyText))

tlacitko.clicked.connect(zmen_text)

hlavni_okno.show()

app.exec()