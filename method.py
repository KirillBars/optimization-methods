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

class HykaJivsa():
    def __init__(self, x1min, x1max, x2min, x2max, x1start, x2start, count_step, y, excpts):
        '''инициализирует атрибуты метода'''
        self.x1min = x1min
        self.x2min = x2min
        self.x1max = x1max
        self.x2max = x2max
        self.count_step = count_step
        self.y = y
        self.excpts = excpts
        self.x1start = x1start
        self.x2start = x2start
        self.imin = 0
        self.jmin = 0
        self.kol = 0
        self.min = self.y_func(self.x1start, self.x2start)
        self.x1top = 0
        self.x1bot = 0
        self.x1left = 0
        self.x1right = 0
        self.top_bot_bool = True
        self.list_result = []
        
        self.x1massiv = []
        self.x2massiv = []

        self.x1massiv.append(self.x1start)
        self.x2massiv.append(self.x2start)


    def y_func(self, x1, x2):
        return float(format(eval(self.y), '.2f'))

    def exception(self, x1, x2):
        '''Проверка ограничений'''
        for i in self.excpts:
            if not eval(i):
                return False
        return True

    def top_bot(self):
        self.x1top = self.x1start + self.count_step
        self.x1bot = self.x1start - self.count_step
        mintop = self.y_func(self.x1top, self.x2start)
        minbot = self.y_func(self.x1bot, self.x2start)

        if self.exception(self.x1top,self.x2start) and self.min > mintop:
            #self.x1start = self.x1top
            self.x1start = float(format(self.x1top, '.2f'))
            self.min = mintop
            
            result = 'x1 = {0} x2 = {1} F(x1,x2) = {2}\n'.format(
                self.x1start, self.x2start, self.min)
            self.list_result.append(result)
            print('x1 = ', self.x1start, ' x2 = ', self.x2start, ' F(x1,x2) = ', self.min, '\n')
            
            '''v massivi'''
            self.x1massiv.append(self.x1start)
            self.x2massiv.append(self.x2start)
        
        elif self.exception(self.x1bot, self.x2start) and self.min > minbot:
            #self.x1start = self.x1bot
            self.x1start = float(format(self.x1bot, '.2f'))
            self.min = minbot
            
            result = 'x1 = {0} x2 = {1} F(x1,x2) = {2}\n'.format(
                self.x1start, self.x2start, self.min)
            self.list_result.append(result)
            print('x1 = ', self.x1start, ' x2 = ', self.x2start, ' F(x1,x2) = ', self.min, '\n')

            '''v massivi'''
            self.x1massiv.append(self.x1start)
            self.x2massiv.append(self.x2start)
        

        else:
            self.top_bot_bool = False

    def left_right(self):
        self.x1left = self.x2start - self.count_step
        self.x1right = self.x2start + self.count_step
        minleft = self.y_func(self.x1start, self.x1left)
        minright = self.y_func(self.x1start, self.x1right)

        if self.exception(self.x1start, self.x1left) and self.min > minleft:
            #self.x2start = self.x1left
            self.x2start = float(format(self.x1left, '.2f'))
            self.min = minleft

            result = 'x1 = {0} x2 = {1} F(x1,x2) = {2}\n'.format(
                self.x1start, self.x2start, self.min)
            self.list_result.append(result)
            print('x1 = ', self.x1start, ' x2 = ', self.x2start, ' F(x1,x2) = ', self.min, '\n')

            '''v massivi'''
            self.x1massiv.append(self.x1start)
            self.x2massiv.append(self.x2start)
        

        elif self.exception(self.x1start, self.x1right) and self.min > minright:
            #self.x2start = self.x1right
            self.x2start = float(format(self.x1right, '.2f'))
            self.min = minright
            result = 'x1 = {0} x2 = {1} F(x1,x2) = {2}\n'.format(
                self.x1start, self.x2start, self.min)
            self.list_result.append(result)
            # print('x1 = ', self.x1start, ' x2 = ', self.x2start, ' F(x1,x2) = ', self.min, '\n') (добавить на форму начальную точку - x1 x2 и начальный и конечный шаги)


            '''v massivi'''
            self.x1massiv.append(self.x1start)
            self.x2massiv.append(self.x2start)
        

        elif not self.top_bot_bool:
            self.count_step = self.count_step / 2
            # print('уменьшение шага')
            self.top_bot_bool = True
        else:
            self.top_bot_bool = True

    def xz(self, bottom_step):
        while self.count_step > bottom_step:
            self.top_bot()
            self.left_right()    
        else:
            return self.x1start, self.x2start, self.min, self.x1massiv, self.x2massiv


class Shtraf():
    def __init__(self, x1min, x1max, x2min, x2max, x1start, x2start, count_step, y, excpts):
        '''инициализирует атрибуты метода'''
        self.x1min = x1min
        self.x2min = x2min
        self.x1max = x1max
        self.x2max = x2max
        self.count_step = count_step
        self.y = y
        self.excpts = excpts
        self.x1start = x1start
        self.x2start = x2start
        self.imin = 0
        self.jmin = 0
        self.kol = 0
        self.min = 0
        self.x1top = 0
        self.x1bot = 0
        self.x2left = 0
        self.x2right = 0
        self.top_bot_bool = True
        self.sum = 0
                
        self.x1massiv = []
        self.x2massiv = []

        self.x1massiv.append(self.x1start)
        self.x2massiv.append(self.x2start)

        self.list_result = []

    def y_func(self, x1, x2):
        return float(format(eval(self.y), '.2f'))

    def exception(self, x1, x2):
        '''Проверка ограничений'''
        for i in self.excpts:
            if not eval(i):
                self.sum = self.sum + 10

    def top_bot(self):
        self.x1top = self.x1start + self.count_step
        self.x1bot = self.x1start - self.count_step

        self.sum = 0
        self.exception(self.x1top, self.x2start)
        mintop = self.y_func(self.x1top, self.x2start) + (self.sum * self.sum)

        self.sum = 0
        self.exception(self.x1bot, self.x2start)
        minbot = self.y_func(self.x1bot, self.x2start) + (self.sum * self.sum)

        if self.min > mintop:
            self.x1start = self.x1top
            self.min = mintop
            result = 'x1 = {0} x2 = {1} F(x1,x2) = {2}\n'.format(
                self.x1start, self.x2start, self.min)
            self.list_result.append(result)
            print('x1 = ', self.x1start, ' x2 = ', self.x2start, ' F(x1,x2) = ', self.min, '\n')
            
            '''v massivi'''
            self.x1massiv.append(self.x1start)
            self.x2massiv.append(self.x2start)

        elif self.min > minbot:
            self.x1start = self.x1bot
            self.min = minbot
            result = 'x1 = {0} x2 = {1} F(x1,x2) = {2}\n'.format(
                self.x1start, self.x2start, self.min)
            self.list_result.append(result)
            print('x1 = ', self.x1start, ' x2 = ', self.x2start, ' F(x1,x2) = ', self.min, '\n')

            '''v massivi'''
            self.x1massiv.append(self.x1start)
            self.x2massiv.append(self.x2start)

        else:
            self.top_bot_bool = False

    def left_right(self):
        self.x2left = self.x2start - self.count_step
        self.x2right = self.x2start + self.count_step

        self.sum = 0 
        self.exception(self.x1start, self.x2left)
        minleft = self.y_func(self.x1start, self.x2left) + (self.sum * self.sum)

        self.sum = 0
        self.exception(self.x1start, self.x2right)
        minright = self.y_func(self.x1start, self.x2right) + (self.sum * self.sum)

        if self.min > minleft:
            self.x2start = self.x2left
            self.min = minleft
            result = 'x1 = {0} x2 = {1} F(x1,x2) = {2}\n'.format(
                self.x1start, self.x2start, self.min)
            self.list_result.append(result)
            print('x1 = ', self.x1start, ' x2 = ', self.x2start, ' F(x1,x2) = ', self.min, '\n')

            '''v massivi'''
            self.x1massiv.append(self.x1start)
            self.x2massiv.append(self.x2start)

        elif self.min > minright:
            self.x2start = self.x2right
            self.min = minright
            result = 'x1 = {0} x2 = {1} F(x1,x2) = {2}\n'.format(
                self.x1start, self.x2start, self.min)
            self.list_result.append(result)
            print('x1 = ', self.x1start, ' x2 = ', self.x2start, ' F(x1,x2) = ', self.min, '\n') #(добавить на форму начальную точку - x1 x2 и начальный и конечный шаги)

            '''v massivi'''
            self.x1massiv.append(self.x1start)
            self.x2massiv.append(self.x2start)

        elif not self.top_bot_bool:
            self.count_step = self.count_step / 2
            result = 'уменьшение шага {0}\n'.format(
                self.count_step)

            self.list_result.append(result)
            print('уменьшение шага  ', self.count_step)
            self.top_bot_bool = True
        else:
            self.top_bot_bool = True

    def xz(self, bottom_step):
        self.exception(self.x1start, self.x2start)
        self.min = self.y_func(self.x1start, self.x2start) + (self.sum * self.sum)
        while self.count_step > bottom_step:
            self.top_bot()
            self.left_right()    
        else:
            return self.x1start, self.x2start, self.min, self.x1massiv, self.x2massiv