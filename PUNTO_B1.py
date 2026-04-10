# -- coding: utf-8 --

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys

# --- NUEVA SECCIÃ“N DE HARDWARE PARA PCA9685 ---
try:
    import board
    import busio
    from adafruit_pca9685 import PCA9685
    from adafruit_motor import servo


    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50

    # Definimos los servos en los canales 0 y 1 de la placa azul
    # Ajustamos el pulse_width para que coincida con tus servos anteriores
    SERVO_1 = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)
    SERVO_2 = servo.Servo(pca.channels[1], |min_pulse=500, max_pulse=2500)
    
except Exception as e:
    print(f"Error de Hardware: {e}")
    SERVO_1 = SERVO_2 = None
# ----------------------------------------------

class Ui_MainWindow(object):
    def __init__(self):
        self.ultimo_angulo_1 = -1
        self.ultimo_angulo_2 = -1

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 320)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # --- Labels y UI (Se mantiene igual que tu original) ---
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 0, 341, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 501, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 100, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit.setFont(font)
        
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(20, 150, 481, 31))
        self.horizontalSlider.setMaximum(180)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(290, 100, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        
        # Labels de crÃ©ditos
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 210, 241, 21))
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 190, 121, 16))
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 230, 201, 21))
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(20, 250, 141, 16))
        
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(280, 180, 221, 141))
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(ruta_base, "ecci.jpg")
        self.label_7.setPixmap(QtGui.QPixmap(ruta_logo))
        self.label_7.setScaledContents(True)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

        # ConexiÃ³n del slider
        self.horizontalSlider.valueChanged.connect(self.servos)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Control PCA9685 ECCI"))
        self.label.setText(_translate("MainWindow", "CONTROL DE DOS SERVOMOTORES"))
        self.label_2.setText(_translate("MainWindow", "INGRESE: SERVO 1 o SERVO 2"))
        self.label_4.setText(_translate("MainWindow", "JOHAN SEBASTIAN FAJARDO PIRAQUIVE"))
        self.label_5.setText(_translate("MainWindow", "UNIVERSIDAD ECCI"))
        self.label_6.setText(_translate("MainWindow", "BRAYAN CAMILO ROMERO BERNAL"))
        self.label_8.setText(_translate("MainWindow", "ELECTIVA DE ROBOTICA"))

    def servos(self):
        servo_name = self.textEdit.toPlainText().strip().upper()
        nuevo_angulo = self.horizontalSlider.value()
        umbral = 5

        # LÃ³gica de control usando la nueva librerÃ­a
        if servo_name == "SERVO 1" and SERVO_1:
            if abs(nuevo_angulo - self.ultimo_angulo_1) >= umbral:
                SERVO_1.angle = nuevo_angulo # .angle es compatible con adafruit_servo
                self.ultimo_angulo_1 = nuevo_angulo
                self.label_3.setText(f"Servo 1: {nuevo_angulo}Â°")
        
        elif servo_name == "SERVO 2" and SERVO_2:
            if abs(nuevo_angulo - self.ultimo_angulo_2) >= umbral:
                SERVO_2.angle = nuevo_angulo
                self.ultimo_angulo_2 = nuevo_angulo
                self.label_3.setText(f"Servo 2: {nuevo_angulo}Â°")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
