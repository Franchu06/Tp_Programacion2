from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox
import sys
import hashlib
import mysql.connector
from database import db_config, create_tables

class InsuranceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        create_tables()

    def initUI(self):
        self.setWindowTitle('Sistema de Seguros')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Usuario')
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Contraseña')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton('Registrarse', self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.login_button = QPushButton('Iniciar Sesión', self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def execute_query(self, query, params):
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute(query, params)
        cnx.commit()
        cursor.close()
        cnx.close()

    def register(self):
        username = self.username_input.text()
        password = hashlib.sha256(self.password_input.text().encode()).hexdigest()

        if username and password:
            query = '''INSERT INTO users (username, password) VALUES (%s, %s)'''
            self.execute_query(query, (username, password))
            QMessageBox.information(self, 'Éxito', 'Usuario registrado con éxito!')
        else:
            QMessageBox.warning(self, 'Error', 'Por favor, complete todos los campos')

    def login(self):
        username = self.username_input.text()
        password = hashlib.sha256(self.password_input.text().encode()).hexdigest()

        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        result = cursor.fetchone()

        if result:
            QMessageBox.information(self, 'Éxito', 'Inicio de sesión exitoso!')
        else:
            QMessageBox.warning(self, 'Error', 'Usuario o Contraseña Incorrectos')

        cursor.close()
        cnx.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = InsuranceApp()
    mainApp.show()
    sys.exit(app.exec_())
