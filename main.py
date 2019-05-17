import sys
import math
import random
import pylab, numpy

from PyQt5 import QtCore, QtGui, QtWidgets

from method import Method, MonteCarlo, HykaJivsa, Shtraf
from design import Ui_Form

class Main(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        Form = QtWidgets.QWidget()
        super().__init__()
        self.setupUi(Form)

        '''Massivi'''
        self.x1massiv = []
        self.x2massiv = []


        '''Назначение кнопкам события'''
        self.run_button.clicked.connect(self.calculate)
        self.add_btn.clicked.connect(self.add_exception)
        self.btn_graph.clicked.connect(self.show_graph)
        Form.show()
        sys.exit(app.exec_())

    def show_graph(self):
        xx1 = numpy.arange(self.x1min, self.x1max + self.step, self.step)
        xx2 = numpy.arange(self.x2min, self.x2max + self.step, self.step)

        x1, x2 = numpy.meshgrid(xx1, xx2)
        zgrid = eval(self.function)
        mask = numpy.zeros_like(zgrid, dtype=bool)

        mask[:, :3] = True
        mask[:7, :4] = True
        mask[:4, :5] = True
        mask[:3, :6] = True
        mask[:2, :] = True

        zgrid = numpy.ma.array(zgrid, mask=mask)

        corner_masks = [False, True]
        fig, axs = pylab.subplots()

        for corner_mask in zip(corner_masks):
            
            cs = axs.contourf(x2, x1, zgrid, 30, corner_mask = corner_mask) # или contour
            axs.contour(cs, colors='k')
            axs.grid(c='k', ls='-', alpha=0.3)

            if self.method_CombBox.currentIndex() == 2 or self.method_CombBox.currentIndex() == 3:
                for i in range(len(self.x1_massiv) - 1):

                    if self.x1_massiv[i] != self.x1_massiv[i+1]:

                        axs.vlines(self.x2_massiv[i], self.x1_massiv[i], self.x1_massiv[i+1], colors = 'r')
                    else:
                        axs.hlines(self.x1_massiv[i], self.x2_massiv[i], self.x2_massiv[i+1], colors = 'r')
            
        pylab.show()

    def add_exception(self):
        '''Добавление исключений в таблицу'''
        left_edit = self.exeption_left_edit.text()
        right_edit = self.exeption_right_edit.text()
        if not left_edit or not right_edit:
            QtWidgets.QMessageBox.critical(self, "Ошибка", 'Заполните все поля при добавлении исключений!')
        else:
            kol = self.exeption_table.rowCount()
            self.exeption_table.setRowCount(kol+1)

            tableItem = QtWidgets.QTableWidgetItem("{0} {1} {2}".format(left_edit, self.combBox.currentText(), right_edit))
            self.exeption_table.setItem(0,kol,tableItem)
            

    def calculate(self):
        '''Функция заполнение таблицы '''
        # if __import__('re').findall('\d+? *?\+ *?\d+?', self.objectiv_func_edit.text()):
        #     pass
        # else:
        #     pass

        self.result_table.setColumnCount(0)
        self.result_table.setRowCount(0)

        self.x1min = float(self.x1_min_edit.text())
        self.x1max = float(self.x1_max_edit.text())
        self.x2min = float(self.x2_min_edit.text())
        self.x2max = float(self.x2_max_edit.text())
        self.step  = float(self.step_combBox.currentText())
        self.function = str(self.objectiv_func_edit.text())

        if self.x1min >= self.x1max or self.x2min >= self.x2max:
            QtWidgets.QMessageBox.critical(self, "Ошибка", 'Минимальное значение больше максимального: Xmin > Xmax')
        else:
            self.excpts = []
            # достает существующие ограничения и вносит в список
            for expt in range(0, self.exeption_table.rowCount()):
                if self.exeption_table.item(expt, 0).text():
                    self.excpts.append(self.exeption_table.item(expt, 0).text())

            if self.method_CombBox.currentIndex() == 0:
                self.method_perebor()
            if self.method_CombBox.currentIndex() == 1:
                self.method_montecarlo()
            if self.method_CombBox.currentIndex() == 2:
                self.x1_hyk = float(self.x1_hyk_edit.text())
                self.x2_hyk = float(self.x2_hyk_edit.text())
                self.step_hyk = float(self.step_hyk_edit.text())
                self.bottom_step = float(self.bottom_step_hyk_edit.text())

                self.method_HykaJivsa()
            
            if self.method_CombBox.currentIndex() == 3:
                self.x1_hyk = float(self.x1_hyk_edit.text())
                self.x2_hyk = float(self.x2_hyk_edit.text())
                self.step_hyk = float(self.step_hyk_edit.text())
                self.bottom_step = float(self.bottom_step_hyk_edit.text())
                self.method_Shtraf()

    def method_HykaJivsa(self):
        HykJivs = HykaJivsa(self.x1min, self.x1max, self.x2min, self.x2max, self.x1_hyk, self.x2_hyk, self.step_hyk, self.function, self.excpts)
        x, y, min_x, self.x1_massiv, self.x2_massiv = HykJivs.xz(self.bottom_step)

        list_result = HykJivs.list_result[:]
        str_list_result = ''
        for result in list_result:
            str_list_result += result

        if not str_list_result:
            str_list_result += 'Вы указали точку(х1, х2) вне области определния функции. Решение не найдено'

        QtWidgets.QMessageBox.information(self, 
            "Результат\n", 
            "{0}\n\nМинимум функции:\t{1:.2f}\n\t\tx1:\t{2:.2f}\n\t\tx2:\t{3:.2f}".format(str_list_result, min_x, x, y))
        
            
    def method_perebor(self):
        method = Method(self.x1min, self.x2min, self.x1max, self.x2max, self.step, self.function, self.excpts)
        bool_matrix = method.boolean_matrix
        spis = method.spis

        self.result_table.setColumnCount(len(spis[0]))
        self.result_table.setRowCount(len(spis))
        
        for i in range(len(spis)):
            for j in range(len(spis[i])):
                self.min(i, j, spis, bool_matrix)

        min_value_of_fuction, x1, x2 = method.min_needed()
        QtWidgets.QMessageBox.information(self, 
        "Результат", 
        "Минимум функции:\t{0}\n\tx1:\t{1}\n\tx2:\t{2}".format(min_value_of_fuction, x1, x2))

    def method_montecarlo(self):
        monteCarlo = MonteCarlo(self.x1min, self.x1max, self.x2min, self.x2max, 10, self.function, self.excpts)
        count_shots = 121

        for i in range(count_shots):
            x1, x2 = monteCarlo.rand()
            monteCarlo.func(x1, x2)
        min_value_of_fuction, x1, x2, count_hits = monteCarlo.get_min()
        QtWidgets.QMessageBox.information(self, 
        "Результат", 
        "            Минимум функции:\t{0}\n\t\tx1:\t{1}\n\t\tx2:\t{2}\nКол-во попаданий в ОДЗ:\t{3}\n                Всего испытаний:\t{4}".format(
                                                                                                        min_value_of_fuction, x1, x2, count_hits, count_shots))

    def method_Shtraf(self):
        Shtraff = Shtraf(self.x1min, self.x1max, self.x2min, self.x2max, self.x1_hyk, self.x2_hyk, self.step_hyk, self.function, self.excpts)
        x, y, min_x, self.x1_massiv, self.x2_massiv = Shtraff.xz(self.bottom_step)
        
        list_result = Shtraff.list_result[:]
        str_list_result = ''
        for result in list_result:
            str_list_result += result
                
        QtWidgets.QMessageBox.information(self, 
            "Результат\n", 
            "{0}\n\nМинимум функции:\t{1:.2f}\n\t\tx1:\t{2:.2f}\n\t\tx2:\t{3:.2f}".format(str_list_result,min_x, x, y))

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