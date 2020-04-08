import sys
import os
from form_classes import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainForm()
    wnd.show()
    sys.exit(app.exec())
