# -*- coding: utf-8 -*-
import sys
import smbus2
from PyQt5 import QtCore, QtGui, QtWidgets
import os   

# --- CONFIGURACIÓN DEL SENSOR MPU6050 ---
# Registros del MPU6050
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
BUS_I2C = 1  # Bus 1 en Raspberry Pi
ADDRESS = 0x68 # Dirección estándar I2C del MPU

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(574, 409)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Etiquetas de créditos
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 240, 241, 21))
        self.label_4.setObjectName("label_4")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(40, 280, 141, 16))
        self.label_8.setObjectName("label_8")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 220, 121, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(40, 260, 201, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(300, 210, 221, 141))
        self.label_7.setText("")
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(ruta_base, "ecci.jpg")
        self.label_7.setPixmap(QtGui.QPixmap(ruta_logo))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        
        # Título y etiquetas de entrada
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 10, 331, 21))
        font = QtGui.QFont(); font.setPointSize(16); self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 60, 321, 21))
        font = QtGui.QFont(); font.setPointSize(12); self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        # Input: Edit Text (QTextEdit)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(370, 50, 121, 41))
        font = QtGui.QFont(); font.setPointSize(12); self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        
        # Botón: Push Button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 110, 121, 51))
        font = QtGui.QFont(); font.setPointSize(12); self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        
        # Output: Static Text (QLabel) donde se verá la lectura
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 130, 250, 40))
        font = QtGui.QFont(); font.setPointSize(14); font.setBold(True); self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: blue;")
        self.label_3.setText("")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lectura I2C MPU6050"))
        self.label_4.setText(_translate("MainWindow", "JOHAN SEBASTIAN FAJARDO PIRAQUIVE"))
        self.label_8.setText(_translate("MainWindow", "ELECTIVA DE ROBOTICA"))
        self.label_5.setText(_translate("MainWindow", "UNIVERSIDAD ECCI"))
        self.label_6.setText(_translate("MainWindow", "BRAYAN CAMILO ROMERO BERNAL"))
        self.label.setText(_translate("MainWindow", "LECTURA DE SENSOR POR I2C"))
        self.label_2.setText(_translate("MainWindow", "INGRESE EL TIEMPO DE VISUALIZACION (s)"))
        self.pushButton.setText(_translate("MainWindow", "VISUALIZAR"))

# --- CLASE DE LÓGICA ---
class MpuControl(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Inicializar Bus I2C y MPU
        try:
            self.bus = smbus2.SMBus(BUS_I2C)
            self.bus.write_byte_data(ADDRESS, PWR_MGMT_1, 0) # Despertar sensor
        except Exception as e:
            print(f"Error I2C: {e}")
            self.ui.label_3.setText("Error de Conexión")

        # Configurar Timers
        self.timer_lectura = QtCore.QTimer()
        self.timer_lectura.timeout.connect(self.actualizar_valor)
        
        self.timer_apagado = QtCore.QTimer()
        self.timer_apagado.setSingleShot(True)
        self.timer_apagado.timeout.connect(self.detener_lectura)

        # Conectar Botón
        self.ui.pushButton.clicked.connect(self.procesar_boton)

    def actualizar_valor(self):
        try:
            # Leer aceleración en eje X (registros 0x3B y 0x3C)
            high = self.bus.read_byte_data(ADDRESS, ACCEL_XOUT_H)
            low = self.bus.read_byte_data(ADDRESS, ACCEL_XOUT_H + 1)
            valor = (high << 8) | low
            
            # Formato con signo (complemento a 2)
            if valor > 32768:
                valor -= 65536
            
            self.ui.label_3.setText(f"Eje X: {valor}")
        except:
            self.ui.label_3.setText("Falla lectura")

    def procesar_boton(self):
        try:
            # Leer tiempo desde el Edit Text
            texto_tiempo = self.ui.textEdit.toPlainText().strip()
            tiempo_seg = float(texto_tiempo)
            
            # Iniciar visualización
            self.timer_lectura.start(100) # Actualiza cada 100ms
            self.timer_apagado.start(int(tiempo_seg * 1000)) # Se apaga en N milisegundos
        except ValueError:
            self.ui.label_3.setText("Ingresa un número")

    def detener_lectura(self):
        self.timer_lectura.stop()
        self.ui.label_3.setText("Tiempo agotado")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = MpuControl()
    ventana.show()
    sys.exit(app.exec_())
