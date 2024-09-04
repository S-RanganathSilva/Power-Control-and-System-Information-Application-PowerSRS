import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QLabel, QLineEdit, QDialog, QDialogButtonBox
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
import os
import subprocess

class RunDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Run")
        self.setGeometry(100, 100, 400, 100)

        layout = QVBoxLayout()

        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Type a command and press OK")
        layout.addWidget(self.command_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.run_command)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def run_command(self):
        command = self.command_input.text()
        if command:
            os.system(command)
        self.accept()

class PowerControlApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Power Control and System Information")
        self.setGeometry(100, 100, 700, 500)

        # Set up the black and white theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        # Set logo
        self.setWindowIcon(QIcon("logo.png"))

        # Create the main horizontal layout
        main_layout = QHBoxLayout()

        # Create system information layout
        info_layout = QVBoxLayout()
        info_layout.addWidget(self.create_section_label("System Information"))

        # Create power options layout
        power_layout = QVBoxLayout()
        power_layout.addWidget(self.create_section_label("Power Options"))

        font = QFont('Arial', 12, QFont.Bold)
        button_style = """
        QPushButton {
            border-radius: 10px;
            padding: 15px;
            background-color: #333;
            color: white;
        }
        QPushButton:pressed {
            background-color: #555;
        }
        """

        # System Information Buttons
        info_buttons = [
            ("System Information", self.open_system_info),
            ("Device Manager", self.open_device_manager),
            ("System Properties", self.open_system_properties),
            ("Task Manager", self.open_task_manager),
            ("Command Line Info", self.open_command_line_info),
            ("DirectX Diagnostic", self.open_dxdiag),
            ("Run Dialog", self.open_run_dialog)
        ]

        for text, func in info_buttons:
            button = QPushButton(text, self)
            button.setFont(font)
            button.setStyleSheet(button_style)
            button.clicked.connect(func)
            info_layout.addWidget(button)

        # Power Control Buttons
        power_buttons = [
            ("Shutdown", lambda: self.shutdown(0)),
            ("Shutdown Delay", lambda: self.shutdown(60)),
            ("Restart", lambda: self.restart(0)),
            ("Restart Delay", lambda: self.restart(60)),
            ("Hibernate", self.hibernate),
            ("Sleep", self.sleep),
            ("Abort", self.abort)
        ]
        
        for text, func in power_buttons:
            button = QPushButton(text, self)
            button.setFont(font)
            button.setStyleSheet(button_style)
            button.clicked.connect(func)
            power_layout.addWidget(button)

        # Add both layouts to the main horizontal layout
        main_layout.addLayout(info_layout)
        main_layout.addLayout(power_layout)

        # Set main layout
        self.setLayout(main_layout)

    def create_section_label(self, text):
        """Create a label for section titles."""
        label = QLabel(text)
        label.setFont(QFont('Arial', 14, QFont.Bold))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)
        return label

    # Power Control Functions
    def shutdown(self, delay):
        os.system(f"shutdown /s /f /t {delay}")

    def restart(self, delay):
        os.system(f"shutdown /r /f /t {delay}")

    def hibernate(self):
        os.system("shutdown /h")

    def sleep(self):
        subprocess.call(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])

    def abort(self):
        os.system("shutdown /a")

    # System Information Functions
    def open_system_info(self):
        subprocess.Popen(["msinfo32"])

    def open_device_manager(self):
        subprocess.Popen(["devmgmt.msc"], shell=True)

    def open_system_properties(self):
        subprocess.Popen(["sysdm.cpl"], shell=True)

    def open_task_manager(self):
        subprocess.Popen(["taskmgr"], shell=True)

    def open_command_line_info(self):
        os.system("start cmd /k systeminfo")

    def open_dxdiag(self):
        subprocess.Popen(["dxdiag"])

    def open_run_dialog(self):
        dialog = RunDialog()
        dialog.exec_()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PowerControlApp()
    window.show()
    sys.exit(app.exec_())
