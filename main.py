from camara.face_recognizer import login_capture
from login import gui_login
from PyQt5.QtWidgets import QApplication
import sys


def main():
    # login_capture()
    app = QApplication(sys.argv)
    login_window = gui_login.Estructured()
    login_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
