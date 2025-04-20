import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QPalette, QColor, QIcon, QAction
from fritzconnection import FritzConnection
import json
import os
from cryptography.fernet import Fernet

def set_dark_theme(app: QApplication):
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(55, 99, 99))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    app.setPalette(dark_palette)
    app.setStyleSheet(
        "QToolTip { "
        "color: #ffffff; "
        "background-color: #2a82da; "
        "border: 1px solid white; "
        "}"
    )

CONFIG_FILE = "config.json"
KEY_FILE = "config.key"

def get_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

fernet = Fernet(get_key())

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"ip": "192.168.178.1", "username": "test", "password": "test"}
    try:
        with open(CONFIG_FILE, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode("utf-8"))
    except Exception as e:
        # If the file is corrupted, a default configuration is returned
        print(f"Error loading configuration: {e}")
        return {"ip": "192.168.178.1", "username": "test", "password": "test"}

config = load_config()

FRITZBOX_IP = config["ip"]
USERNAME = config["username"]
PASSWORD = config["password"]

def save_config(config):
    try:
        data = json.dumps(config).encode("utf-8")
        encrypted_data = fernet.encrypt(data)
        with open(CONFIG_FILE, "wb") as f:
            f.write(encrypted_data)
    except Exception as e:
        print(f"Error saving configuration: {e}")

class SettingsDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.config = config

        layout = QFormLayout()
        self.ip_edit = QLineEdit(self.config["ip"])
        self.user_edit = QLineEdit(self.config["username"])
        self.pass_edit = QLineEdit(self.config["password"])
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("IP Address:", self.ip_edit)
        layout.addRow("Username:", self.user_edit)
        layout.addRow("Password:", self.pass_edit)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def save_settings(self):
        try:
            self.config["ip"] = self.ip_edit.text()
            self.config["username"] = self.user_edit.text()
            self.config["password"] = self.pass_edit.text()
            save_config(self.config)
            QMessageBox.information(self, "Saved", "Settings saved!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving settings:\n{e}")

def wlan_on():
    try:
        fc = FritzConnection(address=config["ip"], user=config["username"], password=config["password"])
        fc.call_action("WLANConfiguration:1", "SetEnable", NewEnable=True)
        info = fc.call_action("WLANConfiguration:1", "GetInfo")
        if info["NewEnable"]:
            return "WLAN ON ✅"
        else:
            return "WLAN could not be enabled."
    except Exception as e:
        return f"Error enabling WLAN: {e}"

def wlan_off():
    try:
        fc = FritzConnection(address=config["ip"], user=config["username"], password=config["password"])
        fc.call_action("WLANConfiguration:1", "SetEnable", NewEnable=False)
        info = fc.call_action("WLANConfiguration:1", "GetInfo")
        if not info["NewEnable"]:
            return "WLAN OFF ❌"
        else:
            return "WLAN could not be disabled."
    except Exception as e:
        return f"Error disabling WLAN: {e}"

def main():
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)  

    set_dark_theme(app)
    icon = QIcon.fromTheme("network-wireless")
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setToolTip("FritzBox WLAN Control")
    tray.setVisible(True)

    menu = QMenu()

    wlan_on_action = QAction("WLAN ON")
    wlan_on_action.setObjectName("wlan_on_action")
    def wlan_on_triggered():
        msg = wlan_on()
        tray.showMessage("Status", msg)
    wlan_on_action.triggered.connect(wlan_on_triggered)
    menu.addAction(wlan_on_action)

    wlan_off_action = QAction("WLAN OFF")
    wlan_off_action.setObjectName("wlan_off_action")
    def wlan_off_triggered():
        msg = wlan_off()
        tray.showMessage("Status", msg)
    wlan_off_action.triggered.connect(wlan_off_triggered)
    menu.addAction(wlan_off_action)

    menu.addSeparator()

    settings_action = QAction("Settings")
    def open_settings():
        dlg = SettingsDialog(config)
        dlg.exec()
    settings_action.triggered.connect(open_settings)
    menu.addAction(settings_action)

    menu.addSeparator()

    quit_action = QAction("Quit")
    def quit_app():
        tray.hide()
        app.quit()
    quit_action.triggered.connect(quit_app)
    menu.addAction(quit_action)

    menu.setStyleSheet("""
        QMenu { background-color: #000; color: white; }
        QMenu::item#wlan_on_action { background-color: #008000; color: white; }
        QMenu::item#wlan_off_action { background-color: #B22222; color: white; }
        QMenu::item:selected#wlan_on_action { background-color: #00cc00; color: #fff; }
        QMenu::item:selected#wlan_off_action { background-color: #ff4444; color: #fff; }
        QMenu::item:selected { background-color: #444; }
    """)

    tray.setContextMenu(menu)
    app.exec()

if __name__ == "__main__":
    main()
