import json
import subprocess
from PyQt5 import QtWidgets, QtCore
import untiled
import sys

class ChangePasswordDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Зміна паролю")
        
        layout = QtWidgets.QVBoxLayout(self)
        
        self.account_combo = QtWidgets.QComboBox(self)
        self.fill_accounts_combo()
        layout.addWidget(self.account_combo)
        
        self.old_password_edit = QtWidgets.QLineEdit(self)
        self.old_password_edit.setPlaceholderText("Старий пароль")
        layout.addWidget(self.old_password_edit)
        
        self.new_password_edit = QtWidgets.QLineEdit(self)
        self.new_password_edit.setPlaceholderText("Новий пароль")
        layout.addWidget(self.new_password_edit)
        
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def fill_accounts_combo(self):
        accounts = load_accounts()
        for account in accounts:
            self.account_combo.addItem(account)

    def get_data(self):
        return (
            self.account_combo.currentText(),
            self.old_password_edit.text(),
            self.new_password_edit.text()
        )

class ChangeAccountDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Зміна акаунту")
        
        layout = QtWidgets.QVBoxLayout(self)
        
        self.old_account_edit = QtWidgets.QLineEdit(self)
        self.old_account_edit.setPlaceholderText("Старий акаунт")
        layout.addWidget(self.old_account_edit)
        
        self.old_password_edit = QtWidgets.QLineEdit(self)
        self.old_password_edit.setPlaceholderText("Пароль")
        layout.addWidget(self.old_password_edit)
        
        self.new_account_edit = QtWidgets.QLineEdit(self)
        self.new_account_edit.setPlaceholderText("Новий акаунт")
        layout.addWidget(self.new_account_edit)
        
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return (
            self.old_account_edit.text(),
            self.old_password_edit.text(),
            self.new_account_edit.text()
        )

class profil(QtWidgets.QMainWindow, untiled.Ui_MainWindow):
    def __init__(self):
        super(profil, self).__init__()
        self.setupUi(self)
        self.label.setText('Виберіть дію')
        self.pushButton.setText('Змінити пароль')
        self.pushButton_2.setText('Змінити назву акаунту')
        self.pushButton_3.setText('Створення профілю')
        self.pushButton_4.setText('Видалити акаунт')
        self.pushButton_5.setText('Знайти профіль')
        
        self.pushButton.clicked.connect(self.change_password_dialog)
        self.pushButton_2.clicked.connect(self.change_account_dialog)
        self.pushButton_3.clicked.connect(self.open_profile_file)
        self.pushButton_4.clicked.connect(self.delete_account_dialog)
        self.pushButton_5.clicked.connect(self.view_profile)

    def open_profile_file(self):
        subprocess.Popen(["python", "prof_1.py"])

    def change_password_dialog(self):
        dialog = ChangePasswordDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            account, old_password, new_password = dialog.get_data()
            self.change_password(account, old_password, new_password)

    def change_account_dialog(self):
        dialog = ChangeAccountDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            old_account, old_password, new_account = dialog.get_data()
            self.change_account(old_account, old_password, new_account)

    def change_password(self, account, old_password, new_password):
        accounts = load_accounts()
        if account in accounts and accounts[account]['Password'] == old_password:
            accounts[account]['Password'] = new_password
            save_accounts(accounts)
            QtWidgets.QMessageBox.information(self, "Зміна паролю", "Пароль успішно змінено!")
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Введено неправильний старий пароль!")

    def change_account(self, old_account, old_password, new_account):
        accounts = load_accounts()
        profiles = load_profiles()

        if old_account in accounts and accounts[old_account]['Password'] == old_password:
            if new_account in accounts:
                QtWidgets.QMessageBox.warning(self, "Помилка", "Така назва акаунту вже існує!")
            else:
                # Оновлюємо назву акаунту в файлі akaunt.json
                accounts[new_account] = accounts.pop(old_account)
                save_accounts(accounts)

                # Оновлюємо назву акаунту у файлі profiles.json
                if old_account in profiles:
                    profiles[new_account] = profiles.pop(old_account)
                    save_profiles(profiles)

                QtWidgets.QMessageBox.information(self, "Зміна акаунту", "Назва акаунту успішно змінена!")
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Введено неправильний обліковий запис або пароль!")

    def view_profile(self):
        account, ok = QtWidgets.QInputDialog.getText(self, 'Перегляд профілю', 'Введіть назву акаунту:')
        if ok:
            profiles = load_profiles()
            if account in profiles:
                profile = profiles[account]
                profile_info = f"Ім'я: {profile['name']}\n" \
                              f"Вік: {profile['age']}\n" \
                              f"Опис: {profile['description']}"
                QtWidgets.QMessageBox.information(self, "Профіль користувача", profile_info)
            else:
                QtWidgets.QMessageBox.warning(self, "Помилка", f"Акаунт '{account}' не знайдений.")

    def delete_account_dialog(self):
        account, ok = QtWidgets.QInputDialog.getText(self, 'Видалення акаунту', 'Введіть назву акаунту:')
        if ok:
            password, ok = QtWidgets.QInputDialog.getText(self, 'Видалення акаунту', 'Введіть пароль:', QtWidgets.QLineEdit.Password)
            if ok:
                if self.check_password(account, password):
                    reply = QtWidgets.QMessageBox.question(self, 'Видалення акаунту', f"Ви впевнені, що хочете видалити акаунт {account}?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                    if reply == QtWidgets.QMessageBox.Yes:
                        self.delete_account(account, password)
                else:
                    QtWidgets.QMessageBox.warning(self, "Помилка", "Введено неправильний пароль!")

    def check_password(self, account, password):
        accounts = load_accounts()
        if account in accounts and accounts[account]['Password'] == password:
            return True
        else:
            return False

    def delete_account(self, account, password):
        accounts = load_accounts()
        if account in accounts and accounts[account]['Password'] == password:
            del accounts[account]
            save_accounts(accounts)

            profiles = load_profiles()
            if account in profiles:
                del profiles[account]
                save_profiles(profiles)

            QtWidgets.QMessageBox.information(self, "Видалення акаунту", f"Акаунт {account} успішно видалений!")
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Введено неправильний обліковий запис або пароль!")

def load_accounts():
    try:
        with open('akaunt.json', 'r') as file:
            accounts = json.load(file)
    except FileNotFoundError:
        accounts = {}
    return accounts

def save_accounts(accounts):
    with open('akaunt.json', 'w') as file:
        json.dump(accounts, file, indent=4)

def load_profiles():
    try:
        with open('profiles.json', 'r') as file:
            profiles = json.load(file)
    except FileNotFoundError:
        profiles = {}
    return profiles

def save_profiles(profiles):
    with open('profiles.json', 'w') as file:
        json.dump(profiles, file, indent=4)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = profil()
    window.show()
    sys.exit(app.exec_())