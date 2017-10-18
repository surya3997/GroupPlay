from choose import Ui_Choose
from PyQt4 import QtCore, QtGui

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Choose()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

