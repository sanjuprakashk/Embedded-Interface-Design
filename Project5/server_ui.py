# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(720, 505)
        self.imageView = QtWidgets.QLabel(Dialog)
        self.imageView.setGeometry(QtCore.QRect(40, 50, 291, 251))
        self.imageView.setText("")
        self.imageView.setScaledContents(True)
        self.imageView.setObjectName("imageView")
        self.getImageButton = QtWidgets.QPushButton(Dialog)
        self.getImageButton.setGeometry(QtCore.QRect(130, 370, 99, 30))
        self.getImageButton.setObjectName("getImageButton")
        self.getPercentVoiceButton = QtWidgets.QPushButton(Dialog)
        self.getPercentVoiceButton.setGeometry(QtCore.QRect(460, 130, 181, 31))
        self.getPercentVoiceButton.setObjectName("getPercentVoiceButton")
        self.percentCorrectVoiceDisplay = QtWidgets.QLabel(Dialog)
        self.percentCorrectVoiceDisplay.setGeometry(QtCore.QRect(480, 80, 71, 21))
        self.percentCorrectVoiceDisplay.setObjectName("percentCorrectVoiceDisplay")
        self.percentWrongVoiceDisplay = QtWidgets.QLabel(Dialog)
        self.percentWrongVoiceDisplay.setGeometry(QtCore.QRect(560, 80, 71, 21))
        self.percentWrongVoiceDisplay.setObjectName("percentWrongVoiceDisplay")
        self.percentCorrectImagesDisplay = QtWidgets.QLabel(Dialog)
        self.percentCorrectImagesDisplay.setGeometry(QtCore.QRect(480, 260, 71, 21))
        self.percentCorrectImagesDisplay.setObjectName("percentCorrectImagesDisplay")
        self.getPercentImagesButton = QtWidgets.QPushButton(Dialog)
        self.getPercentImagesButton.setGeometry(QtCore.QRect(460, 310, 181, 31))
        self.getPercentImagesButton.setObjectName("getPercentImagesButton")
        self.percentWrongImagesDisplay = QtWidgets.QLabel(Dialog)
        self.percentWrongImagesDisplay.setGeometry(QtCore.QRect(560, 260, 71, 21))
        self.percentWrongImagesDisplay.setObjectName("percentWrongImagesDisplay")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.getImageButton.setText(_translate("Dialog", "Get Image"))
        self.getPercentVoiceButton.setText(_translate("Dialog", "Get % voice commands"))
        self.percentCorrectVoiceDisplay.setText(_translate("Dialog", "% correct"))
        self.percentWrongVoiceDisplay.setText(_translate("Dialog", "% wrong"))
        self.percentCorrectImagesDisplay.setText(_translate("Dialog", "% correct"))
        self.getPercentImagesButton.setText(_translate("Dialog", "Get % images"))
        self.percentWrongImagesDisplay.setText(_translate("Dialog", "% wrong"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

