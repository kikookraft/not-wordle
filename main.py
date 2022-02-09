## Written in python 3.8.5 with pygame 2.0.0

import pygame
import pygame_gui
import random

class game():
    def __init__(self):
        game.screen_size=(900,800)
        game.w = self.screen_size[0]
        game.h = self.screen_size[1]
        game.bg_color='#141414'
        game.FPS = 60
        game.window_surface = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        game.background = pygame.Surface(self.screen_size)
        game.background.fill(pygame.Color(self.bg_color))
        game.is_running = True
        game.clock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption('Not Wordle')
        game.manager = pygame_gui.UIManager(self.screen_size)
        game.texts = {}
        game.letters = {}
        game.rect = {}
        game.font = pygame.font.SysFont("res/font/AnonymousPro-Bold.ttf", 24)
        game.tick = 0
        game.started = False
        game.word = ""
        game.guess = []
    
    def beizer(self, x):
        return x**2*(3-2*x)

    def menu_btn(self):
        #self.screen_size = (self.window_surface.get_width(), self.window_surface.get_height())
        center_x = self.screen_size[0]/2
        center_y = self.screen_size[1]/2
        btn_width = 200
        btn_height = 50
        coord_x = center_x - btn_width/2
        coord_y = center_y - btn_height/2
        y_ptage = coord_y/self.screen_size[1]
        self.button_play = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((coord_x, coord_y - 200*y_ptage), (btn_width, btn_height)),text='JOUER',manager=self.manager)
        self.button_words = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((coord_x, coord_y), (btn_width, btn_height)),text='OPTIONS',manager=self.manager)
        self.button_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((coord_x, coord_y + 200*y_ptage), (btn_width, btn_height)),text='NE PLUS JOUER',manager=self.manager)
        self.btn = [self.button_play, self.button_quit, self.button_words]

    def text(self, pos, text, id, color=(255,255,255), size=24, centered=True):
        ft = pygame.font.SysFont("res/font/AnonymousPro-Bold.ttf", size)
        tx = ft.render(text, True, color)
        txt_size = ft.size(text)
        if centered:
            game.texts[str(id)]=(tx, (pos[0]*game.w-(txt_size[0]/2), pos[1]*game.h-(txt_size[1]/2)), txt_size)
        else:
            game.texts[str(id)]=(tx, (pos[0]*game.w, pos[1]*game.h))
        return str(id)

    def put_char(self, txt, idx):
        size = 150
        color = (255,255,255)
        ft = pygame.font.SysFont("res/font/AnonymousPro-Bold.ttf", size)
        txt_size = ft.size(txt)
        while txt_size[0]/game.w > game.rect[idx]['size'][0] or txt_size[1]/game.h > game.rect[idx]['size'][1]:
            size-=1
            ft = pygame.font.SysFont("res/font/AnonymousPro-Bold.ttf", size)
            txt_size = ft.size(txt)
        tx = ft.render(txt, True, color)
        x= game.rect[idx]['pos'][0] + game.rect[idx]['size'][0]/2
        y= game.rect[idx]['pos'][1] + game.rect[idx]['size'][1]/2
        game.letters[str(id)]= {'data':tx,'pos':(x,y)}
        return str(id)

    def update(self):
        self.screen_size = (self.window_surface.get_width(), self.window_surface.get_height())
        game.window_surface = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        pygame.draw.rect(self.window_surface, (20,20,20), (0,0,self.screen_size[0], self.screen_size[1]))
        game.manager = pygame_gui.UIManager(self.screen_size)
        if not self.started:
            for i in self.btn:
                i.kill()
            self.menu_btn()
    
    def start(self):
        self.button_play.kill()
        self.button_quit.kill()
        self.button_words.kill()
        try: del self.texts['0']
        except: pass
        l=[]
        with open("res/fr.txt", 'r') as f:
            for line in f:
                l.append(line.rstrip())
        game.word = random.choice(l)
        l.clear()
        self.texts.clear()
        #self.text((0.5, 0.1), game.word, 1, (0,200,0), 75)
        print(self.word)
        self.game_ui()
        self.started = True

    def draw_rect(self, id, pos, size, color=(50,50,50), keep_ratio = False):
        self.rect[str(id)] = {'pos':pos, 'size':size, 'color':color, 'ratio':keep_ratio}
        return str(id)

    def game_ui(self):
        box_size = 0.9/(len(game.word)*1.33)
        space_between = 0.01
        space_below = 0.02
        lines = len(game.word)
        y_offset = (0.5-(box_size*(lines+1)+space_below*(lines-1))/2)+0.03
        for i in range(lines+1):
            x_offset = 0.5-(box_size*(lines-1)+space_between*lines)/2
            for j in range(lines):
                self.draw_rect("{} {}".format(i,j), (x_offset,y_offset),(box_size,box_size),keep_ratio=True)
                x_offset+= box_size
                if j<lines-1:
                    x_offset+=space_between
            y_offset+=box_size
            if i<lines:
                y_offset+=space_below
    
    def refresh(self):
        for rect in game.rect:
            if game.rect[rect]['ratio']:
                x= game.rect[rect]['pos'][0]*game.w - game.rect[rect]['size'][1]*game.h/2 ## centrer en x
                y= game.rect[rect]['pos'][1]*game.h - game.rect[rect]['size'][1]*game.h/2 ## centrer en y
                box = pygame.Rect(x, y, game.rect[rect]['size'][1]*game.h, game.rect[rect]['size'][1]*game.h)
            else:
                x= game.rect[rect]['pos'][0]*game.w - game.rect[rect]['size'][0]*game.w/2 ## centrer en x
                y= game.rect[rect]['pos'][1]*game.h - game.rect[rect]['size'][1]*game.h/2 ## centrer en y
                box = pygame.Rect(x, y, game.rect[rect]['size'][0]*game.w, game.rect[rect]['size'][1]*game.h)
            pygame.draw.rect(game.window_surface, game.rect[rect]['color'], box)
        for txt in game.texts:
            game.window_surface.blit(game.texts[txt][0], game.texts[txt][1])
        for txt in game.letters:
            game.window_surface.blit(game.texts[txt]['pos'][0], game.texts[txt]['pos'][1])
        


if __name__ == "__main__":
    G = game()
    G.menu_btn()
    G.update()
    G.button_words.disable()
    kik = G.text((0.01,0.01), "By kikookraft", 0, centered=False)
    title = G.text((0.5,0.1), "Defenitly not Wordle", 1, size=50)


    while G.is_running:
        time_delta = G.clock.tick(G.FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                G.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and G.started:
                    G.start()
                    G.update()
                    G.rect.clear()
                    G.game_ui()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            if event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed':
                if event.ui_element == G.button_play and not G.started:
                    G.start()
                if event.ui_element == G.button_words:
                    pass
                if event.ui_element == G.button_quit:
                    pygame.quit()
                    quit()

            if event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
                G.screen_size = (event.w, event.h)
                G.w = event.w
                G.h = event.h
                G.update()
                G.button_words.disable()
                G.rect.clear()
                G.game_ui()
                try:del G.texts[kik]
                except:pass
            G.manager.process_events(event)
        G.manager.update(time_delta)
        G.window_surface.blit(G.background, (0, 0))
        G.manager.draw_ui(G.window_surface)
        G.refresh()
        pygame.display.update()
        G.tick += 1
