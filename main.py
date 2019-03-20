import sys
import math
import random

from PyQt5 import QtCore, QtGui, QtWidgets

from method import Method
from Form1 import Ui_Form

class Main(Ui_Form):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        Form = QtWidgets.QWidget()
        self.setupUi(Form)
        
        '''Назначение кнопкам события'''
        self.run_button.clicked.connect(self.calculate)
        self.add_btn.clicked.connect(self.add_exception)

        Form.show()
        sys.exit(app.exec_())
        
    def add_exception(self):
        '''Добавление исключений в таблицу'''
        self.except_label.setText('')

        if self.exeption_left_edit.text() == '' or self.exeption_right_edit.text() == '':
            self.except_label.setText('Заполните все поля при добавлении исключений!')
        else:
            kol = self.exeption_table.rowCount()
            self.exeption_table.setRowCount(kol+1)

            tableItem = QtWidgets.QTableWidgetItem("{0} {1} {2}".format(self.exeption_left_edit.text(), self.combBox.currentText(), self.exeption_right_edit.text()))
            self.exeption_table.setItem(0,kol,tableItem)

    def calculate(self):
        '''Функция заполнение таблицы '''
        # if __import__('re').findall('\d+? *?\+ *?\d+?', self.objectiv_func_edit.text()):
        #     print ("[SECURITY] It's all okay)")
        # else:
        #     print ("[SECURITY] FUCK YOU!")
        #     return
        
        self.result_table.setColumnCount(0)
        self.result_table.setRowCount(0)
        self.except_label.setText('')

        #
        x1min = float(self.x1_min_edit.text())
        x1max = float(self.x1_max_edit.text())
        x2min = float(self.x2_min_edit.text())
        x2max = float(self.x2_max_edit.text())
        step  = float(self.step_combBox.currentText())
        function = str(self.objectiv_func_edit.text())
        #
        

        if x1min >= x1max or x2min >= x2max:
            self.except_label.setText('Минимальное значение больше максимального !')
        else:

            #
            excpts = []
            # достает существующие ограничения и вносит в список
            #[excpts.append(self.exeption_table.item(expt, 0).text()) for expt in range(0, self.exeption_table.rowCount())]
            for expt in range(0, self.exeption_table.rowCount()):
                if self.exeption_table.item(expt, 0).text():
                    excpts.append(self.exeption_table.item(expt, 0).text())
            #print (excpts)


            self.method = Method(x1min, x2min, x1max, x2max, step, function, excpts)
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
            print(spis[i][j])

        else:
            tableItem = QtWidgets.QTableWidgetItem("{0}".format(spis[i][j]))
            self.result_table.setItem(i,j,tableItem)
            self.result_table.item(i,j).setBackground(QtGui.QColor(140,100,150))
            self.result_table.item(i,j).setForeground(QtGui.QColor(255, 255, 255))

Main()