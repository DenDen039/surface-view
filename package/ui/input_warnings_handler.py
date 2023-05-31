from PyQt5.QtWidgets import QMessageBox, QStyle
class Handler:
    def __init__(self, UI):
        self.parent = UI

    '''
        warning function returns True on "Ok" button and False on "Cancel"
    
    '''
    def warning(self, text: str) -> bool:

        self.parent.console.append(text)
        if not self.parent.hidden_console:
            self.parent.console.append(text)
            return True

        wg = QMessageBox()
        wg.setWindowTitle("Warning")
        wg.setText("Warning")
        wg.setIcon(QMessageBox.Warning)
        wg.setInformativeText(text)
        wg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = wg.exec()

        if result == QMessageBox.Ok:
            return True
        return False

    def error(self, text: str):

        self.parent.console.append(text)
        if not self.parent.hidden_console:
            return

        wg = QMessageBox()
        wg.setWindowTitle("Error")
        wg.setText("Error")
        wg.setIcon(QMessageBox.Critical)
        wg.setInformativeText(text)
        wg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = wg.exec()
        return result


