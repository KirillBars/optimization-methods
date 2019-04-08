import sys
import math
import random
import pylab, numpy

from PyQt5 import QtCore, QtGui, QtWidgets

from method import Method, MonteCarlo
from Form1 import Ui_Form

class Main(Ui_Form):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        Form = QtWidgets.QWidget()
        self.setupUi(Form)
        
        '''Назначение кнопкам события'''
        self.run_button.clicked.connect(self.calculate)
        self.add_btn.clicked.connect(self.add_exception)
        self.btn_graph.clicked.connect(self.show_graph)
        self.btn_rand.clicked.connect(self.show_rand)
        Form.show()
        sys.exit(app.exec_())
    
    def show_rand(self):
        monteCarlo = MonteCarlo(self.x1min, self.x1max, self.x2min, self.x2max, 10, self.function, self.excpts)
        for i in range(121):
            x1, x2 = monteCarlo.rand()
            monteCarlo.func(x1, x2)
        min_list = monteCarlo.get_min()
        self.min_label.setText(str(min_list[:3]))
        self.label.setText(str(min_list[3]))
        #print(monteCarlo.get_min())  

    def show_graph(self):
        xx1 = numpy.arange(self.x1min, self.x1max + self.step, self.step)
        xx2 = numpy.arange(self.x2min, self.x2max + self.step, self.step)
        x1, x2 = numpy.meshgrid(xx1, xx2)

        zgrid = eval(self.function)

        cs = pylab.contour(x1, x2, zgrid)
        #pylab.clabel(cs, colors="black", inline=False)
        pylab.show()

    def add_exception(self):
        '''Добавление исключений в таблицу'''
        self.except_label.setText('')
        left_edit = self.exeption_left_edit.text()
        right_edit = self.exeption_right_edit.text()
        if not left_edit or not right_edit:
            self.except_label.setText('Заполните все поля при добавлении исключений!')
        else:
            kol = self.exeption_table.rowCount()
            self.exeption_table.setRowCount(kol+1)

            tableItem = QtWidgets.QTableWidgetItem("{0} {1} {2}".format(left_edit, self.combBox.currentText(), right_edit))
            self.exeption_table.setItem(0,kol,tableItem)
            

    def calculate(self):
        '''Функция заполнение таблицы '''
        if __import__('re').findall('\d+? *?\+ *?\d+?', self.objectiv_func_edit.text()):
            pass
        else:
            print ("[SECURITY] FUCK YOU!")
            return

        self.result_table.setColumnCount(0)
        self.result_table.setRowCount(0)
        self.except_label.setText('')

        self.x1min = float(self.x1_min_edit.text())
        self.x1max = float(self.x1_max_edit.text())
        self.x2min = float(self.x2_min_edit.text())
        self.x2max = float(self.x2_max_edit.text())
        self.step  = float(self.step_combBox.currentText())
        self.function = str(self.objectiv_func_edit.text())

        if self.x1min >= self.x1max or self.x2min >= self.x2max:
            self.except_label.setText('Минимальное значение больше максимального !')
        else:
            self.excpts = []
            # достает существующие ограничения и вносит в список
            for expt in range(0, self.exeption_table.rowCount()):
                if self.exeption_table.item(expt, 0).text():
                    self.excpts.append(self.exeption_table.item(expt, 0).text())

            self.method = Method(self.x1min, self.x2min, self.x1max, self.x2max, self.step, self.function, self.excpts)
            bool_matrix = self.method.boolean_matrix
            spis = self.method.spis

            self.result_table.setColumnCount(len(spis[0]))
            self.result_table.setRowCount(len(spis))
            
            for i in range(len(spis)):
                for j in range(len(spis[i])):
                    self.min(i, j, spis, bool_matrix)

            self.min_label.setText(str(self.method.min_needed()))
            
    def min(self, i, j, spis, bool_matrix):
        if i == len(spis)-1 or j == 0:
            tableItem = QtWidgets.QTableWidgetItem("{0}".format(spis[i][j]))
            self.result_table.setItem(i,j,tableItem)
            self.result_table.item(i,j).setForeground(QtGui.QColor(140, 100, 150))
            
        elif bool_matrix[i][j]:    
            tableItem = QtWidgets.QTableWidgetItem(str(spis[i][j]))
            self.result_table.setItem(i,j,tableItem)

        else:
            tableItem = QtWidgets.QTableWidgetItem("{0}".format(spis[i][j]))
            self.result_table.setItem(i,j,tableItem)
            self.result_table.item(i,j).setBackground(QtGui.QColor(140,100,150))
            self.result_table.item(i,j).setForeground(QtGui.QColor(255, 255, 255))

Main()