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
        Dialog.resize(669, 414)
        self.imageView = QtWidgets.QLabel(Dialog)
        self.imageView.setGeometry(QtCore.QRect(40, 50, 291, 251))
        self.imageView.setText("")
        self.imageView.setPixmap(QtGui.QPixmap("black_screen.jpg"))
        self.imageView.setScaledContents(True)
        self.imageView.setObjectName("imageView")
        self.getImageButton = QtWidgets.QPushButton(Dialog)
        self.getImageButton.setGeometry(QtCore.QRect(130, 350, 99, 30))
        self.getImageButton.setObjectName("getImageButton")
        self.getPercentButton = QtWidgets.QPushButton(Dialog)
        self.getPercentButton.setGeometry(QtCore.QRect(440, 230, 181, 31))
        self.getPercentButton.setObjectName("getPercentButton")
        self.percentCorrectVoiceDisplay = QtWidgets.QLabel(Dialog)
        self.percentCorrectVoiceDisplay.setGeometry(QtCore.QRect(410, 60, 111, 21))
        self.percentCorrectVoiceDisplay.setObjectName("percentCorrectVoiceDisplay")
        self.percentWrongVoiceDisplay = QtWidgets.QLabel(Dialog)
        self.percentWrongVoiceDisplay.setGeometry(QtCore.QRect(530, 60, 111, 21))
        self.percentWrongVoiceDisplay.setObjectName("percentWrongVoiceDisplay")
        self.percentCorrectImagesDisplay = QtWidgets.QLabel(Dialog)
        self.percentCorrectImagesDisplay.setGeometry(QtCore.QRect(400, 130, 121, 21))
        self.percentCorrectImagesDisplay.setObjectName("percentCorrectImagesDisplay")
        self.percentWrongImagesDisplay = QtWidgets.QLabel(Dialog)
        self.percentWrongImagesDisplay.setGeometry(QtCore.QRect(530, 130, 121, 21))
        self.percentWrongImagesDisplay.setObjectName("percentWrongImagesDisplay")
        self.imageLabel = QtWidgets.QLabel(Dialog)
        self.imageLabel.setGeometry(QtCore.QRect(160, 320, 68, 22))
        self.imageLabel.setObjectName("imageLabel")
        self.lcdPercentCorrectVoice = QtWidgets.QLCDNumber(Dialog)
        self.lcdPercentCorrectVoice.setGeometry(QtCore.QRect(420, 90, 91, 31))
        self.lcdPercentCorrectVoice.setProperty("value", 0.0)
        self.lcdPercentCorrectVoice.setProperty("intValue", 0)
        self.lcdPercentCorrectVoice.setObjectName("lcdPercentCorrectVoice")
        self.lcdPercentWrongVoice = QtWidgets.QLCDNumber(Dialog)
        self.lcdPercentWrongVoice.setGeometry(QtCore.QRect(540, 90, 91, 31))
        self.lcdPercentWrongVoice.setProperty("value", 0.0)
        self.lcdPercentWrongVoice.setProperty("intValue", 0)
        self.lcdPercentWrongVoice.setObjectName("lcdPercentWrongVoice")
        self.lcdPercentCorrectImages = QtWidgets.QLCDNumber(Dialog)
        self.lcdPercentCorrectImages.setGeometry(QtCore.QRect(420, 160, 91, 31))
        self.lcdPercentCorrectImages.setProperty("value", 0.0)
        self.lcdPercentCorrectImages.setProperty("intValue", 0)
        self.lcdPercentCorrectImages.setObjectName("lcdPercentCorrectImages")
        self.lcdPercentWrongImages = QtWidgets.QLCDNumber(Dialog)
        self.lcdPercentWrongImages.setGeometry(QtCore.QRect(540, 160, 91, 31))
        self.lcdPercentWrongImages.setProperty("value", 0.0)
        self.lcdPercentWrongImages.setProperty("intValue", 0)
        self.lcdPercentWrongImages.setObjectName("lcdPercentWrongImages")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.getImageButton.setText(_translate("Dialog", "Get Image"))
        self.getPercentButton.setText(_translate("Dialog", "Get % Correct & Wrong"))
        self.percentCorrectVoiceDisplay.setText(_translate("Dialog", "% correct voice"))
        self.percentWrongVoiceDisplay.setText(_translate("Dialog", " % wrong voice"))
        self.percentCorrectImagesDisplay.setText(_translate("Dialog", "% correct images"))
        self.percentWrongImagesDisplay.setText(_translate("Dialog", "% wrong images"))
        self.imageLabel.setText(_translate("Dialog", "Label"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

