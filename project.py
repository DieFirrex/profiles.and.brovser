import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QTabWidget
import project_1_ui
from PyQt5 import QtCore
import subprocess

AKAUNT_FILE = "akaunt.json"
PROFILE_FILE = "profiles.json"

class PasswordValidator:
    def is_valid(password):
        if len(password) < 8:
            return False
        
        if password.isalpha():
            return False

        return True

def read_akaunts():
    try:
        with open(AKAUNT_FILE, "r") as file:
            akaunts = json.load(file)
    except FileNotFoundError:
        akaunts = {}
    return akaunts

def save_akaunts(akaunts):
    with open(AKAUNT_FILE, "w") as file:
        json.dump(akaunts, file)

def read_profiles():
    try:
        with open(PROFILE_FILE, "r") as file:
            profiles = json.load(file)
    except FileNotFoundError:
        profiles = {}
    return profiles

def save_profiles(profiles):
    with open(PROFILE_FILE, "w") as file:
        json.dump(profiles, file)

class ProfileDialog(QtWidgets.QDialog):
    def __init__(self, profile_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Профіль')
        self.resize(300, 200)

        layout = QtWidgets.QVBoxLayout(self)

        if "name" in profile_data:
            name_text = profile_data["name"]
            if len(name_text) > 20:
                name_text = '\n'.join([name_text[i:i+20] for i in range(0, len(name_text), 20)])
            name_label = QtWidgets.QLabel(f'Ім\'я: {name_text}')
            name_label.setStyleSheet("color: white; font-size: 14pt;")
            layout.addWidget(name_label)
        else:
            name_label = QtWidgets.QLabel("Ім'я: Не вказано")
            name_label.setStyleSheet("color: white; font-size: 14pt;")
            layout.addWidget(name_label)

        if "age" in profile_data:
            age_label = QtWidgets.QLabel(f'Вік: {profile_data["age"]}')
            age_label.setStyleSheet("color: white; font-size: 14pt;")
            layout.addWidget(age_label)
        else:
            age_label = QtWidgets.QLabel("Вік: Не вказано")
            age_label.setStyleSheet("color: white; font-size: 14pt;")
            layout.addWidget(age_label)

        if "description" in profile_data:
            description_text = profile_data["description"]
            if len(description_text) > 20:
                description_text = '\n'.join([description_text[i:i+20] for i in range(0, len(description_text), 20)])
            description_label = QtWidgets.QLabel(f'Опис: {description_text}')
            description_label.setStyleSheet("color: white; font-size: 14pt;")
            description_label.setWordWrap(True)
            layout.addWidget(description_label, alignment=QtCore.Qt.AlignBottom)
        else:
            description_label = QtWidgets.QLabel("Опис: Не вказано")
            description_label.setStyleSheet("color: white; font-size: 14pt;")
            description_label.setWordWrap(True)
            layout.addWidget(description_label, alignment=QtCore.Qt.AlignBottom)


class AccountsWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Список акаунтів')
        self.resize(300, 200)
        layout = QtWidgets.QVBoxLayout(self)
        self.accounts_list = QtWidgets.QListWidget()
        layout.addWidget(self.accounts_list)
        self.load_accounts()

    def load_accounts(self):
        akaunts = read_akaunts()
        for username in akaunts.keys():
            self.accounts_list.addItem(username)

class Register(QtWidgets.QMainWindow, project_1_ui.Ui_MainWindow):
    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Реєстрація')
        self.lineEdit.setPlaceholderText('Введіть Логін')
        self.lineEdit_2.setPlaceholderText('Введіть Пароль')
        self.pushButton.setText('Реєстрація')
        self.pushButton_2.setText('Вхід')
        self.pushButton_4.setText('Показати акаунти')
        self.pushButton_3.setText('Мій профіль')
        self.setWindowTitle('Реєстрація')
        self.pushButton.pressed.connect(self.register_account) 
        self.pushButton_2.pressed.connect(self.login)
        self.pushButton_4.clicked.connect(self.show_accounts)
        self.pushButton_3.clicked.connect(self.show_profile)

    def show_accounts(self):
        self.accounts_window = AccountsWindow()
        self.accounts_window.show()

    def login(self):
        self.login = Login()
        self.login.show()
        self.hide()

    def show_profile(self):
        username = self.lineEdit.text().strip()
        profiles = read_profiles()
        profile_data = profiles.get(username)
        if profile_data:
            profile_dialog = ProfileDialog(profile_data, parent=self)
            profile_dialog.exec_()
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Не вдалося знайти профіль для цього акаунту.")

    def register_account(self):
        login = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()
        if login and password:
            if PasswordValidator.is_valid(password):
                akaunts = read_akaunts()
                if login in akaunts:
                    QtWidgets.QMessageBox.warning(self, "Помилка", "Акаунт з таким ім'ям вже існує.")
                    return
                akaunts[login] = {
                    'Password': password
                }
                save_akaunts(akaunts)

                profiles = read_profiles()
                profiles[login] = {
                    'Name': '',
                    'Age': 0,
                    'Description': ''
                }
                save_profiles(profiles)
                QtWidgets.QMessageBox.information(self, "Реєстрація", "Акаунт успішно створено!")
            else:
                QtWidgets.QMessageBox.warning(self, "Помилка", "Ви впевнені, що хочете використати такий ненадійний пароль?")
                return
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Будь ласка, введіть логін та пароль.")

class Login(QtWidgets.QMainWindow, project_1_ui.Ui_MainWindow):
    logged_in = False
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Логін')
        self.lineEdit.setPlaceholderText('Введіть логін')
        self.lineEdit_2.setPlaceholderText('Введіть пароль')
        self.pushButton.setText('Вхід')
        self.pushButton_2.setText('Реєстрація')
        self.pushButton_4.setText('Показати акаунти')
        self.pushButton_3.setText('Мій профіль')
        self.setWindowTitle('Вхід')
        self.pushButton_4.clicked.connect(self.show_accounts)
        self.pushButton.pressed.connect(self.login_attempt)
        self.pushButton_2.pressed.connect(self.reg)
        self.pushButton_3.clicked.connect(self.show_profile)

    def show_accounts(self):
        if self.logged_in:
            self.accounts_window = AccountsWindow()
            self.accounts_window.show()
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Будь ласка, увійдіть в систему для перегляду акаунтів.")

    def reg(self):
        if self.logged_in:
            self.reg = Register()
            self.reg.show()
            self.hide()
        else:
            self.label.setText('Спочатку увійдіть в систему!')

    def show_profile(self):
        if self.logged_in:
            username = self.lineEdit.text().strip()
            profiles = read_profiles()
            profile_data = profiles.get(username)
            if profile_data:
                profile_dialog = ProfileDialog(profile_data, parent=self)
                profile_dialog.exec_()
            else:
                QtWidgets.QMessageBox.warning(self, "Помилка", "Не вдалося знайти профіль для цього акаунту.")
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Будь ласка, увійдіть в систему для перегляду профілю.")

    def login_attempt(self):
        user_login = self.lineEdit.text().strip()
        user_password = self.lineEdit_2.text().strip()
        if user_login and user_password:
            akaunts = read_akaunts()
            if user_login in akaunts:
                if akaunts[user_login]['Password'] == user_password:
                    self.logged_in = True
                    QtWidgets.QMessageBox.information(self, "Успішний вхід", "Ви успішно увійшли в систему.")
                    subprocess.Popen(['python', 'okno.py'])
                else:
                    QtWidgets.QMessageBox.warning(self, "Помилка", "Неправильний пароль.")
            else:
                reply = QtWidgets.QMessageBox.question(self, 'Помилка', 'Акаунт не знайдено. Хочете створити новий акаунт?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    self.reg = Register()
                    self.reg.show()
                    self.hide()
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Будь ласка, введіть логін та пароль.")

def is_logged_in():
    return hasattr(Login, 'logged_in') and Login.logged_in

App = QtWidgets.QApplication([])
window = Login()
window.show()
App.exec()
