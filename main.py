import sys
import pygame
import vec
import cube
import text
import core
import coloring
import activator

WIDTH = 768
HEIGHT = 512
CENTER = vec.Vec(HEIGHT // 2, HEIGHT // 2)
TOPLEFT = vec.Vec(5, 5)
SIZE = 32
DIST = SIZE * 3**0.5
CUBE_ARG = True
CONSOLA_TTF = "C:\Windows\Fonts\consola.ttf"
CUBE_KEYS = {
    "w": [0, False],
    "e": [1, False],
    "d": [2, False],
    "s": [3, False],
    "a": [4, False],
    "q": [5, False],
}
VEC_KEYS = {"w": [2, False], "d": [1, False], "s": [0, False], "a": [3, False]}
KEY_MAPS = {
    pygame.K_w: "w",
    pygame.K_e: "e",
    pygame.K_q: "q",
    pygame.K_a: "a",
    pygame.K_s: "s",
    pygame.K_d: "d",
}
mouse_pos = cube.Cube()
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH + 10, HEIGHT + 10))
anim_frame = 0


def cube_valid(cube_pos, size):
    cube_center = cube.Cube(size // 2 + 1, size // 2 + 1)
    return 0 < abs(cube_pos - cube_center) < size // 2


def vec_valid(vec_pos, size):
    return 0 <= vec_pos[0] < size and 0 <= vec_pos[1] < size


def special_vec_valid(vec_pos, size):
    return (0 <= vec_pos[0] < size and 0 <= vec_pos[1] < size) and (
        (vec_pos[0] != size // 2 and vec_pos[1] != size // 2)
        or (
            vec_pos[0] == 0
            or vec_pos[0] == size - 1
            or vec_pos[1] == 0
            or vec_pos[1] == size - 1
        )
    )


games = (
    [
        core.Core(cube.Cube, cube.CUBE_SIDES, cube_valid, CUBE_KEYS, i * 2 - 1)
        for i in range(4, 7)
    ]
    + [core.Core(vec.Vec, vec.VEC_SIDES, vec_valid, VEC_KEYS, i) for i in range(3, 9)]
    + [core.Core(vec.Vec, vec.VEC_SIDES, special_vec_valid, VEC_KEYS, 7)]
)
game_texts = (
    [f"Hexagon (size={str(i)})" for i in range(3, 6)]
    + [f"Square (size={str(i)})" for i in range(3, 9)]
    + [f"Crossed (size=7)"]
)

game_id = 0
for tmp_game in games:
    tmp_game.gen_new()
    tmp_game.gen_new()


def switch_to_board(index):
    global game_id, games, SIZE, DIST
    game_id = index
    game = games[game_id]
    if game.type_iter == cube.Cube:
        SIZE = int(HEIGHT / (game.size - 2) / 3)
        DIST = SIZE * 3**0.5
    elif game.type_iter == vec.Vec:
        SIZE = int(HEIGHT / game.size / 2)
        DIST = SIZE * 3**0.5
    if not game.check():
        reset_board(index)


def reset_board(index):
    if index is None:
        index = game_id
    games[index] = games[index].copy()
    games[index].gen_new()
    games[index].gen_new()


buttons = []
for h_start in [100]:
    for h_delta in [(HEIGHT - h_start) / len(game_texts)]:
        for i in range(len(game_texts)):
            buttons.append(
                activator.Activator(
                    pygame.rect.Rect(
                        (HEIGHT + 10, h_start + i * h_delta), (WIDTH - HEIGHT, h_delta)
                    ).inflate(-20, -5),
                    switch_to_board,
                    index=i,
                )
            )
reset_button = activator.Activator(
    pygame.rect.Rect((HEIGHT + 20, 10), (100, 80)), reset_board, index=None
)


def draw_game_grid(iter, name, size=None):
    game = games[game_id]
    if size is None:
        size = SIZE
    if type(iter) == cube.Cube:
        cube_center = cube.Cube(game.size // 2 + 1, game.size // 2 + 1)
        tmp_center = CENTER + (iter - cube_center).to_pixel(CUBE_ARG, True) * DIST
        draw_flat_hexagon(tmp_center, size - 2, color=coloring.get_color(name)[1])
        if name is not None:
            text.drawbox(
                str(name),
                fontname=CONSOLA_TTF,
                rect=pygame.rect.Rect(
                    tmp_center - vec.Vec(size, size), size * vec.Vec(2, 2)
                ),
                color=coloring.get_color(name)[0],
            )
    elif type(iter) == vec.Vec:
        tmp_topleft = TOPLEFT + iter * SIZE * 2
        pygame.draw.rect(
            screen,
            coloring.get_color(name)[1],
            pygame.rect.Rect(tmp_topleft, 2 * vec.Vec(SIZE, SIZE))
            .inflate(-5, -5)
            .inflate(2 * (size - SIZE), 2 * (size - SIZE)),
        )
        if name is not None:
            text.drawbox(
                str(name),
                fontname=CONSOLA_TTF,
                rect=pygame.rect.Rect(tmp_topleft, 2 * vec.Vec(SIZE, SIZE))
                .inflate(-20, -30)
                .inflate(size - SIZE, size - SIZE),
                color=coloring.get_color(name)[0],
            )


def draw_flat_hexagon(center, size, color=(0, 255, 0)):
    points = []
    for side in cube.CUBE_SIDES:
        point = side.to_pixel(not CUBE_ARG, True) * size
        points.append(point + center)
    pygame.draw.polygon(screen, color, points)


def update():
    global anim_frame
    game = games[game_id]
    clock.tick()
    anim_frame += 0.1
    for event in pygame.event.get():  # 获取事件
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key_unicode = KEY_MAPS.get(event.key, "")
            if key_unicode in game.keys.keys():
                if game.user_move(game.side_iters[game.keys[key_unicode][0]]):
                    anim_frame = 0
            elif event.unicode in "0123456789" and event.unicode:
                switch_to_board(int(event.unicode))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.check(event.pos):
                    button.call()
            if reset_button.check(event.pos):
                reset_button.call()


def draw():
    game = games[game_id]
    screen.fill(coloring.BACKGROUND)
    if anim_frame >= len(game.lst_anims):
        draw_game_board()
    else:
        draw_anim_game_board()
    text.draw(
        "Score:\n%8d" % game.score,
        topright=(WIDTH, 5),
        fontname=CONSOLA_TTF,
        fontsize=36,
    )
    draw_sidebar()


def draw_game_board():
    game = games[game_id]
    for i in range(game.size):
        for j in range(game.size):
            if game.valid(game.type_iter(i, j), game.size):
                draw_game_grid(game.type_iter(i, j), (game[i, j][0]))


def draw_anim_game_board():
    game = games[game_id]
    for i in range(game.size):
        for j in range(game.size):
            if game.valid(game.type_iter(i, j), game.size):
                draw_game_grid(game.type_iter(i, j), None)
    cur_state = int(anim_frame)
    cur_time = anim_frame - cur_state
    for anim in game.lst_anims[cur_state]:
        if type(anim) == core.AnimMove:
            draw_game_grid(
                (anim.iter * cur_time + anim.from_iter * (1 - cur_time)),
                anim.name,
                SIZE,
            )
        elif type(anim) == core.AnimMerge:
            draw_game_grid(
                anim.iter, anim.name, SIZE * (1 + 0.5 * cur_time * (1 - cur_time))
            )
        elif type(anim) == core.AnimAppear:
            draw_game_grid(anim.iter, anim.name, SIZE * (0.25 + 0.75 * cur_time))
        else:
            draw_game_grid(anim.iter, anim.name)


def draw_sidebar():
    for i in range(len(buttons)):
        button = buttons[i]
        if i == game_id:
            pygame.draw.rect(
                screen, coloring.get_color(4)[1], button.rect.inflate(4, 4)
            )
        pygame.draw.rect(screen, coloring.get_color(None)[1], button.rect)
        text.draw(
            game_texts[i],
            topright=vec.Vec(0, 5) + button.rect.topright,
            fontname=CONSOLA_TTF,
        )
    pygame.draw.rect(screen, "#cebeb0", reset_button.rect)
    text.drawbox("Reset", reset_button.rect.inflate(-20, -10), fontname=CONSOLA_TTF)


def tick():
    update()
    draw()
    pygame.display.update()


switch_to_board(0)
while True:
    tick()
    pygame.time.delay(5)
