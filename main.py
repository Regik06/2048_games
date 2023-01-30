import random
import sys
from logics import * #импортируем все из логикс
import pygame
from database import get_best, insert_result, cur #импортируем значения из бд
pygame.init()
GAMERS_DB = get_best()


def draw_top_gamers(): #ф-я для отрисовки топовых игроков в плашке
    font_top = pygame.font.SysFont('simsun', 30) #главная запись вверху
    font_gamer = pygame.font.SysFont('simsun', 24) #имена игрока
    text_head = font_top.render('Best tries: ', True, COLOR_TEXT)
    screen.blit(text_head, (250, 15))
    for index, gamer in enumerate(GAMERS_DB):
        name, score = gamer
        s = f'{index + 1}. {name} - {score}'
        text_gamer = font_gamer.render(s, True, COLOR_TEXT)
        screen.blit(text_gamer, (250, 40 + 20 * index))
        print(index, name, score)


def draw_interface(score, delta=0): #прописываем графику
    pygame.draw.rect(screen, WHITE, TITLE_REC) #фон плашки
    font = pygame.font.SysFont('stxingkai', 70) # шрифт
    font_score = pygame.font.SysFont('simsun', 48) #шрифт цвет и размер надписи
    font_delta = pygame.font.SysFont('simsun', 32)
    text_score = font_score.render('Score: ', True, COLOR_TEXT)
    text_score_value = font_score.render(f'{score}', True, COLOR_TEXT)
    screen.blit(text_score, (20, 35)) #прикрепляем к месту на экране (текст, координаты)
    screen.blit(text_score_value, (150, 35))
    if delta > 0: #если значение(баллы) имеются, то выводим их
        text_delta = font_delta.render(f'+{delta}', True, COLOR_DELTA)
        screen.blit(text_delta, (150, 65))
    pretty_print(mas)
    draw_top_gamers()
    for row in range(BLOCKS): #отрисовка квадратиков
        for column in range(BLOCKS): #по столбцам
            value = mas[row][column] # цифра
            text = font.render(f'{value}', True, BLACK) #цвет цифры
            w = column * SIZE_BLOCKS + (column + 1) * MARGIN #ширина квадрата с цифрой включая отступы
            h = row * SIZE_BLOCKS + (row + 1) * MARGIN + SIZE_BLOCKS # высота включая отступы
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCKS, SIZE_BLOCKS))
            if value != 0: # если значение не 0
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCKS - font_w) / 2
                text_y = h + (SIZE_BLOCKS - font_h) / 2
                screen.blit(text, (text_x, text_y))


 # сам массив

COLOR_TEXT = (1, 128, 128)
COLOR_DELTA = (0, 160, 160)
COLORS = {
    0: (80, 80, 80),
    2: (255, 235, 235),
    4: (255, 199, 199),
    8: (255, 163, 163),
    16: (255, 122, 122),
    32: (184, 255, 255),
    64: (0, 209, 209),
    128: (242, 214, 255),
    256: (117, 60, 144),
    512: (250, 245, 86),
    1024: (147, 1, 84),
    2048: (0, 128, 128),
}

WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
BLACK = (0, 0, 0)

BLOCKS = 4
SIZE_BLOCKS = 110
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCKS + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + 110
TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)


def init_const():
    global score, mas
    mas = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    empty = get_empty_list(mas)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_number(random_num1)
    mas = insert_2_or_4(mas, x1, y1)
    x2, y2 = get_index_from_number(random_num2)
    mas = insert_2_or_4(mas, x2, y2)
    score = 0

mas = None
score = None
USERNAME = None
init_const()

print(get_empty_list(mas))
pretty_print(mas)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')


def draw_intro():
    img2048 = pygame.image.load('2048.png') #добавили заставку
    font = pygame.font.SysFont('stxingkai', 70)  # шрифт
    text_welcome = font.render('Welcome)', True, WHITE)
    name = 'Введите имя'
    is_find_name = False  # переменная для завершения цикла while описывающего событи
    while not is_find_name: #бесконечный цикл описывающий события
        for event in pygame.event.get():  # описываем события
            if event.type == pygame.QUIT:  # если кнопка закрыть
                pygame.quit()  # закрываем
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Введите имя':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE: # удаляем 'text'
                    name = name[:-1]
                elif event.key == pygame.K_RETURN: #проверяем ввел ли пользователь имя
                    if len(name) >= 1:
                        global USERNAME
                        USERNAME = name
                        is_find_name = True
                        break


        screen.fill(BLACK)
        text_name = font.render(name, True, WHITE)
        rect_name = text_name.get_rect() #узнаем где этот прямоугольник текста
        rect_name.center = screen.get_rect().center # устанавливаем по центру экрана
        screen.blit(pygame.transform.scale(img2048, [200, 200]), [10, 10])
        screen.blit(text_welcome, (240, 80))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)


def draw_game_over():
    global USERNAME, mas
    img2048 = pygame.image.load('2048.png')  # добавили заставку
    font = pygame.font.SysFont('stxingkai', 70)  # шрифт
    text_game_over = font.render(f'Game Over', True, WHITE)
    text_score = font.render(f'Вы набрали: {score}', True, WHITE)
    best_score = GAMERS_DB[0][1]
    if score > best_score:
        text = 'Рекорд побит!'
    else:
         text = f'Рекорд: {best_score}'
    text_record = font.render(text, True, WHITE)
    insert_result(USERNAME, score)
    make_desicion = False
    while not make_desicion: #бесконечный цикл описывающий события
        for event in pygame.event.get():  # описываем события
            if event.type == pygame.QUIT:  # если кнопка закрыть
                pygame.quit()  # закрываем
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # restart game width name
                    make_desicion = True
                    init_const()
                elif event.key == pygame.K_RETURN:
                    # new game new name
                    USERNAME = None
                    make_desicion = True
                    init_const()

        screen.fill(BLACK)
        screen.blit(text_game_over, (220, 40))
        screen.blit(text_score, (30, 250))
        screen.blit(text_record, (30, 300))
        screen.blit(pygame.transform.scale(img2048, [200, 200]), [10, 10])
        pygame.display.update()
    screen.fill(BLACK)


def game_loop(): #игровой цикл
    global score, mas
    draw_interface(score)
    pygame.display.update()

    while is_zero_from_mas(mas) or can_move(mas):  # цикл главной игры
        for event in pygame.event.get():  # описываем события
            if event.type == pygame.QUIT:  # если кнопка закрыть
                pygame.quit()  # закрываем
                sys.exit(0)  # выходим из программы
            elif event.type == pygame.KEYDOWN:  # иначе если нажимаем на клавиатуре
                delta = 0
                if event.key == pygame.K_LEFT:  # левая кнопка - функция срабатывает
                    mas, delta = move_left(mas)
                elif event.key == pygame.K_RIGHT:
                    mas, delta = move_right(mas)
                elif event.key == pygame.K_UP:
                    mas, delta = move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas, delta = move_down(mas)
                score += delta
                if is_zero_from_mas(mas):
                    empty = get_empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_number(random_num)
                    mas = insert_2_or_4(mas, x, y)
                    print(f'мы заполнили элемент {random_num}')
                draw_interface(score, delta)
                pygame.display.update()


while True:
    if USERNAME is None:
        draw_intro()# вызов начальной заставки
    game_loop()
    draw_game_over()
