import pygame
from copy import deepcopy
from random import choice, randrange
from greedy import greedy_best_move
from a_star import astar_best_move

# إعدادات اللعبة
W, H = 10, 20
TILE = 25
GAME_RES = W * TILE, H * TILE
RES = 430, 540
FPS = 60

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

# الخلفيات
bg1 = pygame.image.load("i/b1.png").convert()
bg2 = pygame.image.load("i/b2.png").convert()
backgrounds = [bg1, bg2]

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

# أشكال التيترس
figures_pos = [
    [(-1, 0), (-2, 0), (0, 0), (1, 0)],
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, 0)],
]
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig] for fig in figures_pos]

get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
main_font = pygame.font.SysFont("comicsansms", 40)
font = pygame.font.SysFont("arial", 25)


# أزرار
def draw_button(surface, text, rect, color, hover_color, mouse_pos, click):
    pygame.draw.rect(surface, hover_color if rect.collidepoint(mouse_pos) else color, rect)
    label = font.render(text, True, pygame.Color("black"))
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)
    return rect.collidepoint(mouse_pos) and click


def get_record():
    try:
        with open("record") as f:
            return f.readline()
    except:
        with open("record", "w") as f:
            f.write("0")
        return "0"


def set_record(record, score):
    rec = max(int(record), score)
    with open("record", "w") as f:
        f.write(str(rec))


def reset_game():
    return deepcopy(choice(figures)), deepcopy(choice(figures)), get_color(), get_color(), [[0 for _ in range(W)] for _
                                                                                            in range(H)], 0, 60, 2000, 0


def start_screen():
    bg_index = 0
    start = False
    while not start:
        sc.blit(backgrounds[bg_index], (0, 0))
        title = main_font.render("TRIO VIBES ", True, pygame.Color("gold"))
        sc.blit(title, (RES[0] // 2 - title.get_width() // 2, 60))

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        start_rect = pygame.Rect(115, 200, 200, 50)
        exit_rect = pygame.Rect(115, 270, 200, 50)
        if draw_button(sc, "Start", start_rect, pygame.Color("white"), pygame.Color("lightgray"), mouse_pos, click):
            start = True
        if draw_button(sc, "Exit", exit_rect, pygame.Color("gold"), pygame.Color("orange"), mouse_pos, click):
            pygame.quit()
            exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                bg_index = (bg_index + 1) % len(backgrounds)

        pygame.display.flip()
        clock.tick(FPS)


start_screen()

figure, next_figure, color, next_color, field, anim_count, anim_speed, anim_limit, score = reset_game()
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


# --------- MAIN LOOP ---------
def is_valid_move(figure, field):
    """ التحقق من أن القطعة لا تتداخل مع قطع أخرى أو تتجاوز حدود الميدان """
    for f in figure:
        if not (0 <= f.x < W and 0 <= f.y < H) or field[f.y][f.x]:
            return False
    return True


def drop_figure(figure, field):
    """ إسقاط القطعة إلى أدنى نقطة ممكنة """
    while True:
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
        if not is_valid_move(figure, field):
            figure = deepcopy(figure_old)
            break
    return figure


def move_figure_to_lowest_possible(figure, field):
    """حركة القطعة إلى أدنى مكان ممكن في الميدان"""
    min_y = min(f.y for f in figure)  # أبعد نقطة يمكن أن تصل إليها القطعة
    while True:
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
        if not is_valid_move(figure, field):
            figure = deepcopy(figure_old)
            break
    return figure


while True:
    record = get_record()
    dx, rotate = 0, False
    sc.blit(backgrounds[0], (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True

    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
    if not is_valid_move(figure, field):
        figure = deepcopy(figure_old)

    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
        if not is_valid_move(figure, field):
            for f in figure_old:
                field[f.y][f.x] = color
            figure, color = next_figure, next_color
            next_figure, next_color = deepcopy(choice(figures)), get_color()
            anim_limit = 2000

    center = figure[0]
    if rotate:
        figure_old = deepcopy(figure)
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
        if not is_valid_move(figure, field):
            figure = deepcopy(figure_old)

    # معالجة الصفوف المكتملة وإزالةها
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = sum(1 for x in field[row] if x)
        if count < W:
            field[line] = field[row][:]  # نقل الصف
            line -= 1
        else:
            lines += 1
            field[line] = [0] * W  # إزالة الصف المكتمل
            line -= 1

    # تحريك الصفوف فوق الصف المكتمل للأسفل
    for row in range(line, -1, -1):
        for col in range(W):
            if field[row][col]:
                field[row + lines][col] = field[row][col]
                field[row][col] = 0

    score += scores[lines]

    [pygame.draw.rect(game_sc, (40, 40, 40), i, 1) for i in grid]
    for f in figure:
        figure_rect.topleft = f.x * TILE, f.y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell:
                figure_rect.topleft = x * TILE, y * TILE
                pygame.draw.rect(game_sc, cell, figure_rect)
    for f in next_figure:
        figure_rect.topleft = f.x * TILE + 210, f.y * TILE + 90
        pygame.draw.rect(sc, next_color, figure_rect)

    sc.blit(main_font.render("TETRIS", True, pygame.Color("gold")), (270, 20))

    # زر Greedy
    greedy_rect = pygame.Rect(270, 440, 130, 40)
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    if draw_button(sc, "Use Greedy", greedy_rect, pygame.Color("lightblue"), pygame.Color("cyan"), mouse_pos, click):
        figure = greedy_best_move(figure, field, color)

    sc.blit(font.render("Score:", True, pygame.Color("white")), (280, 350))
    sc.blit(font.render(str(score), True, pygame.Color("white")), (300, 380))
    sc.blit(font.render("Record:", True, pygame.Color("white")), (280, 250))
    sc.blit(font.render(record, True, pygame.Color("gold")), (300, 280))

    # زر A*
    astar_rect = pygame.Rect(270, 490, 130, 40)
    if draw_button(sc, "Use A*", astar_rect, pygame.Color("lightgreen"), pygame.Color("green"), mouse_pos, click):
        figure = astar_best_move(figure, field, color)

    if any(field[0]):
        set_record(record, score)
        sc.blit(font.render("Game Over", True, pygame.Color("red")), (150, 180))
        restart_rect = pygame.Rect(115, 250, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if draw_button(sc, "Restart", restart_rect, pygame.Color("white"), pygame.Color("lightgray"), mouse_pos, click):
            figure, next_figure, color, next_color, field, anim_count, anim_speed, anim_limit, score = reset_game()

    pygame.display.flip()
    clock.tick(FPS)
