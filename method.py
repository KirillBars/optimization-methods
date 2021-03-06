import random

class Method():
    def __init__(self, x1min, x2min, x1max, x2max, step, y, excpts):
        '''инициализирует атрибуты метода'''
        self.x1min = x1min
        self.x2min = x2min
        self.x1max = x1max
        self.x2max = x2max
        self.step = step
        self.y = y
        self.excpts = excpts

        self.columns = (x2max - x2min) / step + 1
        self.lines = (x1max - x1min) / step + 1
        self.setting_up_a_frame_spis()
        self.bool_matrix()
        self.setting_midle_spis()

    def setting_up_a_frame_spis(self):
        '''создаёт двумерный список нужного размера заполненный нулями'''
        self.spis = [[0 for i in range(int(self.columns + 1))] for j in range(int(self.lines + 1))]

        for line in range(int(self.lines)):
            self.spis[line][0] = float(format(self.step*(int(self.lines) - line - 1) + self.x1min, '.2f'))

        for column in range(1, int(self.columns + 1)):
            self.spis[int(self.lines)][column] = float(format(self.step*(column - 1) + self.x2min, '.2f'))

        self.spis[int(self.lines)][0] = 'x1/x2'

    def y_func(self, x1, x2):
        return float(format(eval(self.y), '.2f'))
    
    def setting_midle_spis(self):
        '''заполнение середины списка'''
        for line in range(int(self.lines)):
            for column in range(1, int(self.columns + 1)):
               x1 = self.spis[line][0] 
               x2 = self.spis[int(self.lines)][column]

               self.spis[line][column] = self.y_func(x1, x2)
               self.exception(x1, x2, line, column)

    def bool_matrix(self):
        '''Создание булевой матрицы'''
        self.boolean_matrix = [[False for i in range(int(self.columns + 1))] for j in range(int(self.lines))] 

    def exception(self, x1, x2, row, col):
        '''Проверка ограничений'''
        b =  True
        for i in self.excpts:
            if not eval(i):
                b = False
                return
        
        self.boolean_matrix[row][col] = True 

    def min_needed(self):
        '''Нахождение минимального значения, подходящего под ограничения'''
        self.min = 999999
        for line in range(int(self.lines)):
            for column in range(1, int(self.columns + 1)):
                if self.boolean_matrix[line][column] and self.spis[line][column] < self.min:
                    self.min = self.spis[line][column]
                    imin = line
                    jmin = column
        '''Если нету элементов подходящих под ограничения'''
        if self.min == 999999:
            return

        return self.min, self.spis[imin][0], self.spis[int(self.lines)][jmin]

class MonteCarlo():
    def __init__(self, x1min, x1max, x2min, x2max, count_step, y, excpts):
        '''инициализирует атрибуты метода'''
        self.x1min = x1min
        self.x2min = x2min
        self.x1max = x1max
        self.x2max = x2max
        self.count_step = count_step
        self.y = y
        self.excpts = excpts
        self.min = 999999
        self.imin = 0
        self.jmin = 0
        self.kol = 0
    
    def rand(self):
        x1 = random.randint(-10, 40) / 10
        x2 = random.randint(-10, 40) / 10

        return x1, x2

    def y_func(self, x1, x2):
        return float(format(eval(self.y), '.2f'))

    def exception(self, x1, x2):
        '''Проверка ограничений'''
        for i in self.excpts:
            if not eval(i):
                return False
        return True


    def func(self, x1, x2):
        if self.exception(x1, x2):
            func_x1_x2 = self.y_func(x1, x2)
            self.kol += 1
            if self.min > func_x1_x2:
                self.min = func_x1_x2
                self.imin = x1
                self.jmin = x2

    def get_min(self):
        return self.min, self.imin, self.jmin, self.kol


    