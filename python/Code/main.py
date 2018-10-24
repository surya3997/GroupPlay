from choose import Ui_Choose
from PyQt5 import QtCore, QtWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Choose()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

