# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(614, 286)
        self.setTempLimitButton = QtWidgets.QPushButton(Dialog)
        self.setTempLimitButton.setGeometry(QtCore.QRect(180, 180, 141, 30))
        self.setTempLimitButton.setObjectName("setTempLimitButton")
        self.tempLimitLine = QtWidgets.QLineEdit(Dialog)
        self.tempLimitLine.setGeometry(QtCore.QRect(30, 180, 113, 32))
        self.tempLimitLine.setClearButtonEnabled(False)
        self.tempLimitLine.setObjectName("tempLimitLine")
        self.setHumLimitButton = QtWidgets.QPushButton(Dialog)
        self.setHumLimitButton.setGeometry(QtCore.QRect(180, 210, 141, 30))
        self.setHumLimitButton.setObjectName("setHumLimitButton")
        self.changeUnitsButton = QtWidgets.QPushButton(Dialog)
        self.changeUnitsButton.setGeometry(QtCore.QRect(400, 90, 99, 30))
        self.changeUnitsButton.setObjectName("changeUnitsButton")
        self.tempDisplayLine = QtWidgets.QLineEdit(Dialog)
        self.tempDisplayLine.setGeometry(QtCore.QRect(180, 40, 131, 31))
        self.tempDisplayLine.setObjectName("tempDisplayLine")
        self.humDisplayLine = QtWidgets.QLineEdit(Dialog)
        self.humDisplayLine.setGeometry(QtCore.QRect(180, 70, 131, 31))
        self.humDisplayLine.setObjectName("humDisplayLine")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 40, 91, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 70, 71, 31))
        self.label_2.setObjectName("label_2")
        self.immediateValButton = QtWidgets.QPushButton(Dialog)
        self.immediateValButton.setGeometry(QtCore.QRect(370, 50, 181, 31))
        self.immediateValButton.setObjectName("immediateValButton")
        self.tempExceededLine = QtWidgets.QLineEdit(Dialog)
        self.tempExceededLine.setGeometry(QtCore.QRect(380, 180, 171, 31))
        self.tempExceededLine.setObjectName("tempExceededLine")
        self.humExceededLine = QtWidgets.QLineEdit(Dialog)
        self.humExceededLine.setGeometry(QtCore.QRect(380, 210, 171, 31))
        self.humExceededLine.setObjectName("humExceededLine")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(140, 0, 111, 31))
        self.label_3.setObjectName("label_3")
        self.timestampDisplayLine = QtWidgets.QLineEdit(Dialog)
        self.timestampDisplayLine.setGeometry(QtCore.QRect(180, 100, 131, 31))
        self.timestampDisplayLine.setObjectName("timestampDisplayLine")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(80, 100, 81, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(410, 150, 121, 31))
        self.label_5.setObjectName("label_5")
        self.humLimitLine = QtWidgets.QLineEdit(Dialog)
        self.humLimitLine.setGeometry(QtCore.QRect(30, 210, 113, 32))
        self.humLimitLine.setClearButtonEnabled(False)
        self.humLimitLine.setObjectName("humLimitLine")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "EID_Project1"))
        self.setTempLimitButton.setText(_translate("Dialog", "Set Temp Limit"))
        self.setHumLimitButton.setText(_translate("Dialog", "Set Hum Limit"))
        self.changeUnitsButton.setText(_translate("Dialog", "ChangeUnits"))
        self.label.setText(_translate("Dialog", "Temperature"))
        self.label_2.setText(_translate("Dialog", "Humidity"))
        self.immediateValButton.setText(_translate("Dialog", "Get Sensor Value"))
        self.label_3.setText(_translate("Dialog", "Sensor Values"))
        self.label_4.setText(_translate("Dialog", "Timestamp"))
        self.label_5.setText(_translate("Dialog", "Alarm Messages"))

