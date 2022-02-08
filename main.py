from re import S
from turtle import screensize
import pygame
import pygame_gui

class game():
    def __init__(self):
        game.screen_size=(900,800)
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
        self.button_words = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((coord_x, coord_y), (btn_width, btn_height)),text='MOTS',manager=self.manager)
        self.button_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((coord_x, coord_y + 200*y_ptage), (btn_width, btn_height)),text='NE PLUS JOUER',manager=self.manager)
        self.btn = [self.button_play, self.button_quit, self.button_words]
    
    def title(self):
        center_x = self.screen_size[0]/2
        center_y = self.screen_size[1]/2
        btn_width = 200
        btn_height = 50
        coord_x = center_x - btn_width/2
        coord_y = center_y - btn_height/2
        y_ptage = coord_y/self.screen_size[1]

    def update(self):
        self.screen_size = (self.window_surface.get_width(), self.window_surface.get_height())
        game.window_surface = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        pygame.draw.rect(self.window_surface, (22,30,30), (0,0,self.screen_size[0], self.screen_size[1]))
        game.manager = pygame_gui.UIManager(self.screen_size)
        for i in self.btn:
            i.kill()
        self.menu_btn()

if __name__ == "__main__":
    G = game()
    G.menu_btn()
    G.update()
    

    while game.is_running:
        time_delta = game.clock.tick(game.FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.is_running = False
            if event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed':
                if event.ui_element == G.button_play:
                    print('Hello World!')

            if event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
                game.screen_size = (event.w, event.h)
                G.update()
            game.manager.process_events(event)

        game.manager.update(time_delta)

        game.window_surface.blit(game.background, (0, 0))
        game.manager.draw_ui(game.window_surface)
        pygame.display.update()
