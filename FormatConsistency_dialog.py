from PyQt5 import uic
from PyQt5 import QtWidgets
import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'FormatConsistency_dialog_base.ui'))

class FormatConsistencyDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(FormatConsistencyDialog, self).__init__(parent)
        self.setupUi(self)
