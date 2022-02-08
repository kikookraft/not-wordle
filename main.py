from tkinter import font
import pygame
import pygame_gui
import random

class game():
    def __init__(self):
        game.screen_size=(900,800)
        game.w = self.screen_size[0]
        game.h = self.screen_size[1]
        game.bg_color='#161E1E'
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
        game.font = pygame.font.SysFont("res/font/AnonymousPro-Bold.ttf", 24)
        game.tick = 0
        game.started = False
        game.word = ""
        game.guess = []

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
            game.texts[str(id)]=(tx, (pos[0]*game.w-(txt_size[0]/2), pos[1]*game.h-(txt_size[1]/2)))
        else:
            game.texts[str(id)]=(tx, (pos[0]*game.w, pos[1]*game.h))

    def update(self):
        self.screen_size = (self.window_surface.get_width(), self.window_surface.get_height())
        game.window_surface = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        pygame.draw.rect(self.window_surface, (22,30,30), (0,0,self.screen_size[0], self.screen_size[1]))
        game.manager = pygame_gui.UIManager(self.screen_size)
        for i in self.btn:
            i.kill()
        self.menu_btn()
    
    def start(self):
        self.button_play.kill()
        self.button_quit.kill()
        self.button_words.kill()
        del self.texts['0']
        l=[]
        with open("res/fr.txt", 'r') as f:
            for line in f:
                l.append(line.rstrip())
        game.word = random.choice(l)
        l.clear()
        self.text((0.5, 0.1), game.word, 1, (0,200,0), 75)
        
        self.started = True


        

if __name__ == "__main__":
    G = game()
    G.menu_btn()
    G.update()
    G.button_words.disable()
    G.text((0.01,0.01), "By kikookraft", 0, centered=False)

    while G.is_running:
        time_delta = G.clock.tick(G.FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                G.is_running = False
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
                G.update()
            G.manager.process_events(event)

        G.manager.update(time_delta)
        G.window_surface.blit(G.background, (0, 0))
        G.manager.draw_ui(G.window_surface)
        for txt in G.texts:
            G.window_surface.blit(G.texts[txt][0], G.texts[txt][1])
        pygame.display.update()
        G.tick += 1
