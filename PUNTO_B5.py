# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import time
import RPi.GPIO as GPIO # Importamos la librería para los pines

# --- CONFIGURACIÓN DEL MOTOR ---
PINS = [17, 18, 27, 22] # IN1, IN2, IN3, IN4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in PINS:
    GPIO.setup(pin, GPIO.OUT)

# Secuencia de medio paso para el motor 28BYJ-48
SECUENCIA = [
    [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0],
    [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1]
]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(564, 354)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 160, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 200, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(30, 220, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8.setObjectName("label_8")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(290, 150, 221, 141))
        self.label_7.setText("")
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(ruta_base, "ecci.jpg")
        self.label_7.setPixmap(QtGui.QPixmap(ruta_logo))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 180, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 20, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 281, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(320, 60, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 100, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 564, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # --- CONEXIÓN DEL BOTÓN CON LA LÓGICA ---
        self.pushButton.clicked.connect(self.mover_motor)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Punto B5 - Motor"))
        self.label_5.setText(_translate("MainWindow", "UNIVERSIDAD ECCI"))
        self.label_6.setText(_translate("MainWindow", "BRAYAN CAMILO ROMERO BERNAL"))
        self.label_8.setText(_translate("MainWindow", "ELECTIVA DE ROBOTICA"))
        self.label_4.setText(_translate("MainWindow", "JOHAN SEBASTIAN FAJARDO PIRAQUIVE"))
        self.label.setText(_translate("MainWindow", "MOTOR PASO A PASO"))
        self.label_2.setText(_translate("MainWindow", "INDIQUE LA CANTIDAD DE VUELTAS"))
        self.pushButton.setText(_translate("MainWindow", "GIRAR"))

    # --- FUNCIÓN PARA MOVER EL MOTOR ---
    def mover_motor(self):
        try:
            vueltas = float(self.textEdit.toPlainText())
            # 512 ciclos de la secuencia equivalen a 1 vuelta (aprox)
            pasos_necesarios = int(vueltas * 512)

            for _ in range(pasos_necesarios):
                for paso in SECUENCIA:
                    for i in range(4):
                        GPIO.output(PINS[i], paso[i])
                    time.sleep(0.001) # Velocidad del giro
            
            # Apagar pines al terminar
            for pin in PINS:
                GPIO.output(pin, 0)
        except ValueError:
            print("Por favor, ingrese un número válido de vueltas.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
