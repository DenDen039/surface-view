# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreatePointWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(101, 186)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.verticalLayout_point1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_point1.setObjectName("verticalLayout_point1")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.point_input_x = QtWidgets.QLineEdit(Form)
        self.point_input_x.setObjectName("point_input_x")
        self.horizontalLayout.addWidget(self.point_input_x)
        self.verticalLayout_point1.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.point_input_y = QtWidgets.QLineEdit(Form)
        self.point_input_y.setObjectName("point_input_y")
        self.horizontalLayout_2.addWidget(self.point_input_y)
        self.verticalLayout_point1.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.point_input_z = QtWidgets.QLineEdit(Form)
        self.point_input_z.setObjectName("point_input_z")
        self.horizontalLayout_3.addWidget(self.point_input_z)
        self.verticalLayout_point1.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_point1)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.applyButton = QtWidgets.QPushButton(Form)
        self.applyButton.setObjectName("applyButton")
        self.verticalLayout.addWidget(self.applyButton)
        self.cancelButton = QtWidgets.QPushButton(Form)
        self.cancelButton.setObjectName("cancelButton")
        self.verticalLayout.addWidget(self.cancelButton)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_7.setText(_translate("Form", "Point:"))
        self.label.setText(_translate("Form", "x:"))
        self.label_2.setText(_translate("Form", "y:"))
        self.label_3.setText(_translate("Form", "z:"))
        self.applyButton.setText(_translate("Form", "Apply"))
        self.cancelButton.setText(_translate("Form", "Cancel"))
