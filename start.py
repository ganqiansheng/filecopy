import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from form import *
from mywin import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = MyWindow()

    main_form.show()

    sys.exit(app.exec())

