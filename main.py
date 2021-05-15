import pygame
import pygame_gui
import os


FPS = 60
LEFT = 10
TOP = 10
CELL = 40

#Importing the external screen
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

#Initializes the screen - Careful: all pygame commands must come after the init
pygame.init()
clock = pygame.time.Clock()


#Sets the screen note: must be after pygame.init()
size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)


class Board(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill((13,13,13))
        self.image.set_colorkey((13,13,13))
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont("monospace", 18)

    def add(self, letter, pos):
        s = self.font.render(letter, 1, (255, 255, 0))
        self.image.blit(s, pos)


class Cursor(pygame.sprite.Sprite):
    def __init__(self, board):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill((0,255,0))
        self.text_height = 17
        self.text_width = 10
        self.rect = self.image.get_rect(topleft=(self.text_width, self.text_height))
        self.board = board
        self.text = ''
        self.cooldown = 0
        self.cooldowns = {'.': 12,
                        '[': 18,
                        ']': 18,
                        ' ': 5,
                        '\n': 30}

    def write(self, text):
        self.text = list(text)

    def update(self):
        if not self.cooldown and self.text:
            letter = self.text.pop(0)
            if letter == '\n':
                self.rect.move_ip((0, self.text_height))
                self.rect.x = self.text_width
            else:
                self.board.add(letter, self.rect.topleft)
                self.rect.move_ip((self.text_width, 0))
            self.cooldown = self.cooldowns.get(letter, 8)

        if self.cooldown:
            self.cooldown -= 1


class Step_Board():
    def __init__(self):
        self.left = LEFT
        self.top = TOP
        self.cell = CELL


    def draw(self, level_map):
        for x in range(len(level_map)):
            for y in range(len(level_map[x])):
                if level_map[x][y] == '.':
                    pygame.draw.rect(screen, pygame.Color('red'), (self.left + self.cell * x, self.top + self.cell * y,
                                                                   self.cell, self.cell), 1)
                elif level_map[x][y] == '#':
                    pygame.draw.rect(screen, pygame.Color('red'), (self.left + self.cell * x, self.top + self.cell * y,
                                                                   self.cell, self.cell))


class Label():
    def __init__(self):
        self.count = 0

    def render(self):
        font = pygame.font.Font('fonts/20354.otf', 100)
        text = font.render('JUST A NEW GAME', True, pygame.Color('white'))
        screen.blit(text, (width // 2 - text.get_size()[0] // 2, height // 8))
        font2 = pygame.font.Font('fonts/20354.otf', 28)
        text2 = font2.render('Author:PYPROJECTGAMES', True, pygame.Color('white'))
        screen.blit(text2, (width // 2 - text2.get_size()[0] // 2, height - height // 8))


manager = pygame_gui.UIManager((width, height), 'theme.json')
btn_play = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width // 3, height // 3,
                                        width // 3, height // 12), manager=manager, text='PLAY')
btn_setting_from_menu = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width // 3, height // 2,
                                        width // 3, height // 12), manager=manager, text='SETTINGS')
btn_exit = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width // 3, height - height // 3,
                                        width // 3, height // 12), manager=manager, text='EXIT')
btn_info = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width // 10, height // 1.2,
                                        width // 8, height // 14), manager=manager, text='INFO')

manager_levels = pygame_gui.UIManager((width, height), 'theme.json')
btn_map_3 = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width - width // 3, height // 3,
                                        width // 6, height // 14), manager=manager_levels, text='MAP 3')
btn_map_3.disable()
btn_map_2 = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width - (width // 3 * 1.75), height // 3,
                                        width // 6, height // 14), manager=manager_levels, text='MAP 2', )
btn_map_2.disable()
btn_map_1 = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width - (width // 3 * 2.5), height // 3,
                                        width // 6, height // 14), manager=manager_levels, text='MAP 1')
btn_back = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width // 10, height // 1.2,
                                        width // 8, height // 14), manager=manager_levels, text='BACK')
manager_game = pygame_gui.UIManager((width, height), 'theme.json')
btn_return = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width // 3, height // 3,
                                        width // 3, height // 12), manager=manager_game, text='RETURN')
btn_setting_from_game = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width // 3, height // 2,
                                        width // 3, height // 12), manager=manager_game, text='SETTINGS')
btn_back_to_menu = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width // 3, height - height // 3,
                                        width // 3, height // 12), manager=manager_game, text='BACK TO MENU')

manager_setting = pygame_gui.UIManager((width, height), 'theme.json')
btn_back_from_set_to_menu = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width // 3, height - height // 3,
                                        width // 3, height // 12), manager=manager_setting, text='BACK TO MENU')
manager_game_finish = pygame_gui.UIManager((width, height), 'theme.json')
btn_finish = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(width // 3, height - height // 3,
                                        width // 3, height // 12), manager=manager_game_finish, text='CONTINUE')

breaf_sprites = pygame.sprite.Group()
secret_sprites = pygame.sprite.Group()
boarded = Step_Board()
main_label = Label()
secret_board = Board()
secret_cursor = Cursor(secret_board)
board = Board()
cursor = Cursor(board)
breaf_sprites.add(cursor, board)
secret_sprites.add(secret_cursor, secret_board)

text = f"""[i] Initializing ...
[i] Entering ghost mode ...
[i] Mastering program ...
[i] Opening new tiles ...
[i] Loading new players ...

done ...

Welcome {os.environ.get( "USERNAME" )} ...

Press 'q' to continue ...

Waiting ...

"""
secret_text = """You should't be here ...
You don't play this game ...
What are you searching?
What you want to find?
You very small for it!
Don't try to find a new info about it ...
Otherwise you will have a problems ...
Big Problemsssssssss ...
Please, be a good person, press 'Q' to continue"""
secret_cursor.write(secret_text)
cursor.write(text)
carts = len(os.listdir(os.chdir('data/fonts')))
os.chdir('..')


class Point(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, level_map):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/sprites/man-2.png').convert_alpha()
        self.level_map = level_map
        for i in range(len(self.level_map)):
            for j in range(len((self.level_map[i]))):
                if self.level_map[i][j] == '@':
                    self.x, self.y = i, j
                    break
        self.rect = self.image.get_rect(topleft=(LEFT + CELL * self.x, TOP + CELL * self.y))
        self.image.set_colorkey('white')
        self.mask = pygame.mask.from_surface(self.image)

    def move_down(self):
        x = (self.rect.left - LEFT) // CELL
        y = (self.rect.top - TOP) // CELL
        level_map[x][y] = '.'
        if self.rect.top == (len(self.level_map[x]) - 1) * CELL + TOP and self.level_map[x][0] != '#':
            self.rect[1] = TOP
        elif self.rect.top == (len(self.level_map[x]) - 1) * CELL + TOP and self.level_map[x][0] == '#':
            pass
        else:
            if self.level_map[x][y + 1] == '#':
                pass
            else:
                self.rect[1] += CELL
        level_map[(self.rect[0] - LEFT) // CELL][(self.rect[1] - TOP) // CELL] = '@'

    def move_up(self):
        x = (self.rect.left - LEFT) // CELL
        y = (self.rect.top - TOP) // CELL
        level_map[x][y] = '.'
        if self.rect.top == TOP and self.level_map[x][len(self.level_map[x]) - 1] != '#':
            self.rect[1] = (len(self.level_map[x]) - 1) * CELL + TOP
        elif self.rect.top == TOP and self.level_map[x][len(self.level_map[x]) - 1] == '#':
            pass
        else:
            if self.level_map[x][y - 1] == '#':
                pass
            else:
                self.rect[1] -= CELL
        level_map[(self.rect[0] - LEFT) // CELL][(self.rect[1] - TOP) // CELL] = '@'

    def move_right(self):
        x = (self.rect.left - LEFT) // CELL
        y = (self.rect.top - TOP) // CELL
        level_map[x][y] = '.'
        if self.rect.left == (len(self.level_map) - 1) * CELL + LEFT and self.level_map[0][y] != '#':
            self.rect[0] = LEFT
        elif self.rect.left == (len(self.level_map) - 1) * CELL + LEFT and self.level_map[0][y] == '#':
            pass
        else:
            if self.level_map[x + 1][y] == '#':
                pass
            else:
                self.rect[0] += CELL
        level_map[(self.rect[0] - LEFT) // CELL][(self.rect[1] - TOP) // CELL] = '@'

    def move_left(self):
        x = (self.rect.left - LEFT) // CELL
        y = (self.rect.top - TOP) // CELL
        level_map[x][y] = '.'
        if self.rect.left == LEFT and self.level_map[len(self.level_map) - 1][y] != '#':
            self.rect[0] = (len(self.level_map) - 1) * CELL + LEFT
        elif self.rect.left == LEFT and self.level_map[len(self.level_map) - 1][y] == '#':
            pass
        else:
            if self.level_map[x - 1][y] == '#':
                pass
            else:
                self.rect[0] -= CELL
        level_map[(self.rect[0] - LEFT) // CELL][(self.rect[1] - TOP) // CELL] = '@'


class Square(pygame.sprite.Sprite):
    def __init__(self, coords):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = coords
        self.image = pygame.image.load('images/sprites/square.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(LEFT + CELL * self.x, TOP + CELL * self.y))


squares = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


#Main loops
breaf = True
main = True
start_page = False
select_levels = False
setting = False
game = False
main_sett = True
level_map = None
secret_scine = False
while main:
    while breaf:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    breaf = False
                    start_page = True
        breaf_sprites.update()
        screen.fill((0, 0, 0))
        breaf_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS * 2)
    while secret_scine:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    secret_scine = False
                    start_page = False
                    breaf = False
                    game = False
                    setting = False
                    select_levels = False
                    main = False
        secret_sprites.update()
        screen.fill((0, 0, 0))
        secret_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS // 2)
    while start_page:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn_exit:
                        breaf = False
                        start_page = False
                        main = False
                        select_levels = False
                        game = False
                        setting = False
                    if event.ui_element == btn_play:
                        start_page = False
                        breaf = False
                        game = False
                        setting = False
                        select_levels = True
                    if event.ui_element == btn_info:
                        textbox = pygame_gui.windows.UIMessageWindow(rect=pygame.rect.Rect(width // 10, height // 3,
                                                                width // 6, height // 6),
                                                                html_message="That's all", manager=manager)
                    if event.ui_element == btn_setting_from_menu:
                        start_page = False
                        breaf = False
                        game = False
                        setting = True
                        select_levels = False
                        main_sett = True
            manager.process_events(event)
        screen.fill((0, 0, 0))
        manager.draw_ui(screen)
        manager.update(FPS)
        main_label.render()
        pygame.display.flip()
    while select_levels:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn_back:
                        breaf = False
                        select_levels = False
                        game = False
                        start_page = True
                        setting = False
                    elif event.ui_element == btn_map_1:
                        with open('maps/map_1.txt', 'r') as mapFile:
                            level_map = [list(line.strip()) for line in mapFile]
                        start_page = False
                        select_levels = False
                        breaf = False
                        game = True
                        setting = False
                    elif event.ui_element == btn_map_2:
                        with open('maps/map_2.txt', 'r') as mapFile:
                            level_map = [list(line.strip()) for line in mapFile]
                        start_page = False
                        select_levels = False
                        breaf = False
                        game = True
                        setting = False
                    elif event.ui_element == btn_map_3:
                        with open('maps/map_3.txt', 'r') as mapFile:
                            level_map = [list(line.strip()) for line in mapFile]
                        start_page = False
                        select_levels = False
                        breaf = False
                        game = True
                        setting = False
            manager_levels.process_events(event)
        screen.fill((0, 0, 0))
        manager_levels.draw_ui(screen)
        manager_levels.update(FPS)
        pygame.display.flip()
    while setting:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn_back_from_set_to_menu:
                        if main_sett:
                            start_page = True
                            select_levels = False
                            breaf = False
                            game = False
                            setting = False
                        else:
                            start_page = False
                            select_levels = False
                            breaf = False
                            game = True
                            setting = False
            manager_setting.process_events(event)
        screen.blit(pygame.image.load('images/backgrounds/back.jpg'), (0, 0))
        manager_setting.draw_ui(screen)
        manager_setting.update(FPS)
        pygame.display.flip()
    if level_map is not None:
        player = Player(level_map)
        all_sprites.add(player)
        for i in range(len(level_map)):
            for j in range(len(level_map[i])):
                if level_map[i][j] == '&':
                    s = Square((i, j))
                    squares.add(s)
                    all_sprites.add(s)
                if level_map[i][j] == '#':
                    pass
    else:
        pass
    while game:
        count = 0
        s = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_menu = True
                    while game_menu:
                        for event_w in pygame.event.get():
                            if event_w.type == pygame.USEREVENT:
                                if event_w.user_type == pygame_gui.UI_BUTTON_PRESSED:
                                    if event_w.ui_element == btn_back_to_menu:
                                        game_menu = False
                                        breaf = False
                                        start_page = True
                                        select_levels = False
                                        game = False
                                        setting = False
                                    if event_w.ui_element == btn_return:
                                        game_menu = False
                                        breaf = False
                                        start_page = True
                                        select_levels = False
                                        game = True
                                        setting = False
                                    if event_w.ui_element == btn_setting_from_game:
                                        game_menu = False
                                        breaf = False
                                        start_page = False
                                        select_levels = False
                                        game = False
                                        setting = True
                                        main_sett = False
                            manager_game.process_events(event_w)
                        screen.fill((0, 0, 0))
                        boarded.draw(level_map)
                        screen.blit(player.image, player.rect)
                        for square in squares:
                            screen.blit(square.image, square.rect)
                        manager_game.draw_ui(screen)
                        manager_game.update(FPS)
                        pygame.display.flip()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_1] and keys[pygame.K_9] and keys[pygame.K_8] and keys[pygame.K_7]:
                    breaf = False
                    start_page = False
                    select_levels = False
                    game = False
                    setting = False
                    main_sett = False
                    secret_scine = True
                if event.key == pygame.K_w:
                    player.move_up()
                if event.key == pygame.K_s:
                    player.move_down()
                if event.key == pygame.K_a:
                    player.move_left()
                if event.key == pygame.K_d:
                    player.move_right()
        screen.fill((0, 0, 0))
        screen.blit(player.image, player.rect)
        for square in squares:
            screen.blit(square.image, square.rect)
        player.update()
        squares.update()
        hint = pygame.sprite.spritecollide(player, squares, True)
        if hint and len(squares.sprites()) == 0:
            game_finish = True
            while game_finish:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == btn_finish:
                                select_levels = True
                                game = False
                                game_finish = False
                    manager_game_finish.process_events(event)
                boarded.draw(level_map)
                manager_game_finish.draw_ui(screen)
                manager_game_finish.update(FPS)
                pygame.display.flip()
            underline = mapFile.name.index('_')
            point = mapFile.name.index('.')          #Понять причину, по которой не исчезает картинка коробки, реализовать инвентарь для переноса коробок, камера за спрайтом
            btns = manager_levels.get_sprite_group().sprites()
            for btn in range(1, len(btns)):
                if str(int(mapFile.name[underline + 1:point]) + 1) == btns[btn].text[len(btns[btn].text) - 1:]:
                    btns[btn].enable()
                    break
        boarded.draw(level_map)
        pygame.display.flip()
pygame.quit()