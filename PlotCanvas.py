#coding=utf-8 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
import pandas as pd

class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=9, height=5, dpi=100):
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.094,right=0.948,top=0.967,bottom=0.094,wspace = 0.2, hspace = 0.257)
        self.chart1 = fig.add_subplot(211)
        self.chart2 = fig.add_subplot(212)
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
 
 
    def plot(self):
        data1 = [0 for i in range(20000)]
        data2 = [0 for i in range(20000)]
        #ax = self.figure.add_subplot(111)
        self.chart1.set_xlim(0,20000)
        self.chart1.set_ylim(0,100)
        self.chart1.plot(data1, 'r-')
        self.chart1.set_xlabel('m/z')
        self.chart1.set_ylabel('Intensity')
        self.chart2.set_xlim(0,20000)
        self.chart2.set_ylim(0,1)
        self.chart2.plot(data2,'b-')
        self.chart2.set_xlabel('m/z')
        self.chart2.set_ylabel('Frequncy')
        #ax.set_title('PyQt Matplotlib Example')
        #self.chart1.set_title('Raw Data')
        #self.chart2.set_title('Peaks Data')
        self.draw()
        
    def plot_raws(self,raws):
        self.chart1.clear()
        #print(raws)
        for i in set(raws.index):
            self.chart1.plot(raws.loc[i]['m/z'],raws.loc[i]['intensity'])
        self.draw()
        
    def plot_ssp(self,ssp):
        self.chart2.clear()
        self.chart2.bar(ssp['m/z'],ssp['count'],width=10)
        self.draw()
        
    def plot_select(self,sp):
        self.chart1.plot(sp['m/z'],sp['intensity'],linestyle='--',color='black')
        self.draw()
        
        
        
        
        
        
        
        