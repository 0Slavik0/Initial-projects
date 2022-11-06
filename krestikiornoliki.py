'''ИГРА "КРЕСТИКИ-НОЛИКИ"
 НАПИСАЛ SLAVIK'''

znach = ['', '0', '1', '2', '00', '01', '02', '10', '11', '12', '20', '21', '22']
X, O, NOUP = 'X', 'O', ' '

def base():
    print("Крестики нолики!")
    board = boardnoup() # создание массива для доски
    firstPl, secondPl = X, O # присваиваем очередь хода

    while True: # основной цикл
        print(boardstr(board))

        otvet = None # запрос значения от игрока
        while not valid(board, otvet):
            print('Куда поставите {}?'.format(firstPl))
            otvet = input("Введите первую цифру столбика, вторую строки\n")
        update(board, otvet, firstPl) # проводим ход

        if win(board, firstPl):
            print(boardstr(board))
            print(f'Выиграл {firstPl}!')
            break

        elif boardfull(board):
            print(boardstr(board))
            print(f'Победила дружба, ничья!')
            break

        firstPl, secondPl = secondPl, firstPl # переход хода

    print('Хорошего дня!')



def boardnoup(): # все клети пустые
    b = {}
    for i in znach:
        b[i] = NOUP
    return b

def boardstr(b): # создание игрового поля в виде текта
    return '''==========
  0  1  2
0 {}  {}  {} 
1 {}  {}  {}
2 {}  {}  {}
=========='''.format(b['00'], b['10'], b['20'],
                     b['01'], b['11'], b['21'],
                     b['02'], b['12'], b['22'])

def valid(b, i): # допуск хода, если в допустимом номере пустая ячейка
    return i in znach and b[i] == NOUP

def boardfull(b):  # при заполнении всех клеток
    for i in znach:
        if b[i] == NOUP:
            return False
    return True

def win(b, p): # выигрышные значения
    return (p == b['00'] == b['11'] == b['22']) or \
           (p == b['20'] == b['11'] == b['02']) or \
           (p == b['00'] == b['01'] == b['02']) or \
           (p == b['10'] == b['11'] == b['12']) or \
           (p == b['20'] == b['21'] == b['22']) or \
           (p == b['00'] == b['10'] == b['20']) or \
           (p == b['01'] == b['11'] == b['21']) or \
           (p == b['02'] == b['12'] == b['22'])

def update(b, i, a): # присваивание значений на поле
    b[i] = a

base()










