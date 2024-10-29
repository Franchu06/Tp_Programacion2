from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit, QLabel
import sys
import hashlib
import mysql.connector
from database import db_config

class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 280, 80)
        
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Usuario')
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Contraseña')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Iniciar Sesión', self)
        self.login_button.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_button)
        
        self.error_label = QLabel('', self)
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def check_credentials(self):
        username = self.username_input.text()
        password = hashlib.sha256(self.password_input.text().encode()).hexdigest()

        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        result = cursor.fetchone()

        if result:
            self.error_label.setText('Login Exitoso!')
        else:
            self.error_label.setText('Usuario o Contraseña Incorrectos')

        cursor.close()
        cnx.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())
