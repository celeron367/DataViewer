#coding=utf-8 
from visualzer import Ui_MainWindow
from data_process import sp_data
from cc_dlg import cc_table
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton,QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon ,QColor
from PyQt5.QtWidgets import QFileDialog
import pandas as pd


class mywindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        super(mywindow,self).__init__(parent)       
        self.setupUi(self)
        
        self.lineEdit_2.setText('1000')
        self.lineEdit_3.setText('5')
        self.lineEdit_4.setText('100')
        self.lineEdit_5.setText('0.05')
        
        self.pushButton.clicked.connect(self.open_path_dlg)
        self.pushButton_2.clicked.connect(self.process_data)
        self.tableWidget.cellClicked.connect(self.table_clk)
        self.pushButton_3.clicked.connect(self.refresh_plot)
        self.pushButton_4.clicked.connect(self.show_cci)
    
             

    def open_path_dlg(self):
        self.work_directory = QFileDialog.getExistingDirectory(self,"选取文件夹","C:/")
        self.lineEdit.setText(self.work_directory)
        self.textBrowser.append('当前数据文件夹：%s' % self.work_directory)
        
    def table_clk(self,row,col):
        #self.widget.plot_raws(self.data.raws)
        select=self.data.raws.loc[row]
        self.widget.plot_select(select)
        #select=QTableWidgetItem(self.data.df.loc[row]['file'])
        #select.setBackground(QColor('Red'))
        #self.tableWidget.setItem(row,0, QTableWidgetItem(select))
        self.tableWidget.item(row,0).setBackground(QColor('Red'))
        
        
        
    def updat_msg(self,msg):
        self.textBrowser.append(msg)
        QApplication.processEvents()
        
    def display_cci(self):
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(self.data.df))
        for i in self.data.df.index:
            self.tableWidget.setItem(i,0, QTableWidgetItem(self.data.df.loc[i]['file']))
            cci=self.data.cc_list.averange(i)
            if (cci<50):
                self.textBrowser_2.append('特异数据：%s' % self.data.df.loc[i]['file'])
            self.tableWidget.setItem(i,1, QTableWidgetItem(str(cci)))
            print(str(cci))
            
    def refresh_plot(self):
        if(self.data is None):
            pass
        else:
            self.widget.plot_raws(self.data.raws)
            
        for i in self.data.df.index:
            self.tableWidget.item(i,0).setBackground(QColor('White'))
            
            
    def process_data(self):
         #self.textBrowser.append('开始分析数据')
         self.textBrowser.clear()
         self.textBrowser_2.clear()
         thresh=float(self.lineEdit_2.text())
         #print(thresh)
         self.data=sp_data(self.work_directory,thresh,self)
         self.updat_msg('归一化.....')
         
         self.data.normallize()
         self.widget.plot_raws(self.data.raws)
         
         self.updat_msg('OK')
         self.updat_msg('寻峰.....')
         
         self.data.peak_search()
         
         self.updat_msg('OK')
         self.updat_msg('生成标准谱.....')

         c_thresh=float(self.lineEdit_5.text())/100
         self.data.state_peaks(c_thresh)
         
         self.updat_msg('OK')
         
         self.widget.plot_ssp(self.data.ssp)
         
         self.updat_msg('计算交叉关联.....')
         self.data.get_cci(0)
         self.display_cci()
         self.updat_msg('分析完成！')
         self.cc_display=cc_table(self.data)
         
    def show_cci(self):
        self.cc_display=cc_table(self.data)


                                     
if __name__ == '__main__':
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    ex = mywindow()
    ex.show()
    
    app.exec_()