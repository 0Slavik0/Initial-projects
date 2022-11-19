'''ИГРА "МОРСКОЙ БОЙ"
 НАПИСАЛ SLAVIK'''

from random import randint


class BoardException(Exception):  # общее исключение
    pass


class OutBoard(BoardException):  # исключение при вводе координат за пределами поля
    def __str__(self):
        return 'Такой координаты не существует!'


class UsedBoard(BoardException):  # исключение при вводе уже использваной точки
    def __str__(self):
        return "По этим координатам уже нанесен удар!"


class WrongShip(BoardException):  # исключение для правильного размещения кораблей
    pass


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # проверка на наличие существующих точек
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # вывод координаты
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, dot, long, orient):
        self.dot = dot
        self.long = long
        self.orient = orient
        self.lives = long

    @property
    def cells(self):  # все координаты корабля на поле с учетом длины и направления
        ship_cells = []
        for i in range(self.long):
            xx = self.dot.x
            yy = self.dot.y

            if self.orient == 1:
                xx += i

            elif self.orient == 0:
                yy += i

            ship_cells.append(Cell(xx, yy))

        return ship_cells

    def shoot(self, shot):  # функц. при попадании
        return shot in self.cells


class GameBoard:
    def __init__(self, hid=False, size=9):
        self.size = size
        self.hid = hid
        self.count = 0  # кол-во пораженных кораблей
        self.busy = []  # список координат занятых кораблями или при попопаданиив эту точку
        self.ships = []  # список кораблей
        self.field = [["◦"] * size for _ in range(size)]  # сетка поля

    def add_ship(self, ship):  # проверка координат корабля на нахождение на поле

        for c in ship.cells:
            if self.out(c) or c in self.busy:
                raise WrongShip()
        for c in ship.cells:
            self.field[c.x][c.y] = "■"
            self.busy.append(c)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):  # метод создает область вокруг координат кораблей
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for c in ship.cells:
            for cx, cy in near:
                cc = Cell(c.x + cx, c.y + cy)
                if not (self.out(cc)) and cc not in self.busy:
                    if verb:
                        self.field[cc.x][cc.y] = "▪"
                    self.busy.append(cc)

    def __str__(self):  # вывод доски
        res = ''
        res += '  | 1  2  3  4  5  6  7  8  9 |\n  _____________________________'
        for i, row in enumerate(self.field):
            res += f'\n{i + 1} | ' + '  '.join(row) + ' |'

        if self.hid:  # скрытие коарблей на поле
            res = res.replace('■', '◦')
        return f'-------------------------------\n{res}\n-------------------------------'

    def out(self, c):  # проверка координат на правильность по отношению к доске
        return not ((0 <= c.x < self.size) and (0 <= c.y < self.size))

    def shot(self, c):  # выстрел по полю
        if self.out(c):
            raise OutBoard()

        elif c in self.busy:
            raise UsedBoard()

        self.busy.append(c)

        for ship in self.ships:
            if c in ship.cells:
                ship.lives -= 1
                self.field[c.x][c.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Товарищ капитан, корабль уничтожен!!!')
                    return True
                else:
                    print('Товарищ капитан, корабль подбит!!!')
                    return True

        self.field[c.x][c.y] = "◌"
        print('Промах!')
        return False

    def begin(self):  # обнуление списка для занесения координат выстрелов
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class User(Player):
    def ask(self):
        while True:
            cords = input('Ваш ход, капитан: ').split()

            if len(cords) != 2:
                print('Необходимо две координаты, капитан! ')
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print('Введите числовые координаты, капитан! ')
                continue

            x, y = int(x), int(y)

            return Cell(x - 1, y - 1)


class AI(Player):
    def ask(self):
        c = Cell(randint(0, 8), randint(0, 8))
        print(f'Ход компьютера: {c.x + 1} {c.y + 1}')
        return c


class Game:
    def __init__(self, size=9):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.us = User(pl, co)
        self.ai = AI(co, pl)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_loc()
        return board

    def random_loc(self):
        lenship = [4, 4, 3, 3, 3, 2, 2, 2, 2, 1, 1]
        board = GameBoard(size=self.size)
        attempts = 0
        for long in lenship:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                ship = Ship(Cell(randint(0, self.size), randint(0, self.size)), long, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except WrongShip:
                    pass
        board.begin()
        return board

    def greet(self):
        print('''
-------------------------------
     Приветсвую вас в игре       
         "МОРСКОЙ БОЙ"          
-------------------------------
       Формат ввода: x y 
       x - номер строки 
       y - номер столбца ''')

    def print_boards(self):
        print(f'-------------------------------\n Доска пользователя:\n{self.us.board}')
        print(f'-------------------------------\n Доска компьютера:\n{self.ai.board}')

    def loops(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                print('''
----------------------
  Ходит пользователь!''')
                repeat = self.us.move()
            else:
                print('''
----------------------
   Ходит компьютер!''')
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                print('''
----------------------
 Выиграл пользватель!''')
                break
            if self.us.board.defeat():
                print('''
----------------------
  Выиграл компьютер!''')
                break
            num += 1

    def start(self):
        self.greet()
        self.loops()


g = Game()
g.start()








#g = GameBoard

#print(g.contour(Cell(2,3),2,0))