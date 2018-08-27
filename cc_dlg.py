# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 10:27:08 2018

@author: Administrator
"""
from ui_cc import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog,QWidget, QFontDialog, QPushButton, QLineEdit, QTableWidgetItem

class cc_table(Ui_Dialog,QDialog):
    def __init__(self,data,parent=None):
        super(cc_table,self).__init__(parent)   
        self.setupUi(self)
        self.tableWidget.setColumnCount(len(data.df))
        self.tableWidget.setRowCount(len(data.df))
        
        for d in data.cc_list.data:
            self.tableWidget.setItem(d[0][0],d[0][1], QTableWidgetItem(str(round(d[1][0],2))))
            self.tableWidget.setItem(d[0][1],d[0][0], QTableWidgetItem(str(round(d[1][0],2))))
            
        self.show()
        