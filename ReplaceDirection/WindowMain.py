import sys
import os
import ReplaceDirectionWindow as RDW
import ReplaceDirectionPkg as RD
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QAbstractItemView, QTableWidgetItem

class WindowWrapper(QWidget, RDW.Ui_ColumnReplace):
    def __init__(self):
        QWidget.__init__(self)

        # define private variables
        self.header = None

        # Set up the user interface from Designer.
        self.setupUi(self)

        # set the table to be not editable
        self.DataPreview.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Make some local modifications.
        self.SelectInput.clicked.connect(self.GetFilePath)
        self.SelectOutput.clicked.connect(self.GetOutputPathOnly)
        self.ReplaceBtn.clicked.connect(self.StartReplace)

    def GetFilePath(self):
        #print("clicked!")
        filenameT = QFileDialog.getOpenFileName(self, 'Select Txt', filter='*.txt')
        if filenameT[0] == '':
            return
        #clear up all data in widget
        self.ClearTable()
        #read in some data to display
        FileData = RD.ReadInFile(filenameT[0], 20)
        if FileData:
            self.AfterGetInputFilePath(FileData)
        else:
            QMessageBox.warning(self, "Warning", "File is not correct!")
            return
        #set up file path in Line
        self.InputFilePath.setText(filenameT[0])
        splitted = os.path.split(filenameT[0])
        AutoTarget = os.path.join(splitted[0], 'A_'+splitted[1])
        self.OutputFilePath.setText(AutoTarget)
        # save header data
        self.header = FileData['header']

    def GetOutputPathOnly(self):
        filenameT = QFileDialog.getOpenFileName(self, 'Select Txt', filter='*.txt')
        self.OutputFilePath.setText(filenameT[0])

    def AfterGetInputFilePath(self, FileData):
        self.DataPreview.setRowCount(FileData['row'])
        self.DataPreview.setColumnCount(FileData['column'])
        self.DataPreview.setHorizontalHeaderLabels(FileData['header'])
        for (i, OneRow) in enumerate(FileData['data']):
            for (j, OneItem) in enumerate(OneRow):
                self.DataPreview.setItem(i, j, QTableWidgetItem(OneItem))

        #set up for combo box
        self.TargetCombo.addItems(FileData['header'])
        self.BackupCombo.addItems(FileData['header'])

    def ClearTable(self):
        self.DataPreview.setRowCount(0)
        self.DataPreview.setColumnCount(0)
        self.DataPreview.clear()
        self.TargetCombo.clear()
        self.BackupCombo.clear()
        self.header = None

    def StartReplace(self):
        TargetColumn = self.header.index(self.TargetCombo.currentText())
        BackupColumn = self.header.index(self.BackupCombo.currentText())
        if (TargetColumn == BackupColumn):
            QMessageBox.critical(self, "Error!", "Can not replace the same Column!!!")
        RD.ReplaceDirection(self.InputFilePath.text(), self.OutputFilePath.text(), TargetColumn, BackupColumn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = WindowWrapper()
    ui.show()
    sys.exit(app.exec_())
