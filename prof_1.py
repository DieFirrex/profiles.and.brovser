import sys
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from prof_ import Ui_MainWindow

class ProfileApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setText("Введіть ім'я")
        self.label_2.setText("Введіть вік")
        self.label_3.setText("Опис себе")
        self.label_4.setText("Редагування профілю")
        self.pushButton.setText('Зберегти')
        self.pushButton.clicked.connect(self.save_profile)

    def save_profile(self):
        name = self.lineEdit.text()
        age = self.spinBox.value()
        description = self.textEdit.toPlainText()

        if name and description:
            account, ok = QInputDialog.getText(self, 'Вибір акаунту', 'Введіть назву акаунту:')
            if ok:
                password, ok = QInputDialog.getText(self, 'Введіть пароль', 'Введіть пароль для акаунту:', QtWidgets.QLineEdit.Password)
                if ok:
                    if self.check_password(account, password):
                        profile = {
                            "name": name,
                            "age": age,
                            "description": description
                        }
                        profiles = {}
                        try:
                            with open('profiles.json', 'r') as file:
                                profiles = json.load(file)
                        except FileNotFoundError:
                            pass
                        profiles[account] = profile
                        with open('profiles.json', 'w') as file:
                            json.dump(profiles, file, indent=4)
                        QMessageBox.information(self, "Збережено", "Ваш профіль успішно збережено!")
                    else:
                        QMessageBox.warning(self, "Помилка", "Неправильний пароль!")
            else:
                QMessageBox.warning(self, "Помилка", "Ім'я та опис обов'язкові до заповнення!")
        else:
            QMessageBox.warning(self, "Помилка", "Ім'я та опис обов'язкові до заповнення!")

    def check_password(self, account, password):
        accounts = self.load_accounts()
        if account in accounts and accounts[account]['Password'] == password:
            return True
        else:
            return False

    def load_accounts(self):
        try:
            with open('akaunt.json', 'r') as file:
                accounts = json.load(file)
        except FileNotFoundError:
            accounts = {}
        return accounts

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ProfileApp()
    window.show()
    sys.exit(app.exec_())