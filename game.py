import pygame #2.1.2
import pygame_gui #0.6.4
import random
from datetime import datetime

class game():
    def __init__(self):
        game.screen_size=(900,800)
        game.color_good = (70,170,50)
        game.color_almost = (220,180,40)
        game.color_bad = (60,30,30)
        self.w = self.screen_size[0]
        self.h = self.screen_size[1]
        game.bg_color='#141414'
        game.general_font = "res/font/UbuntuMono-Bold.ttf"
        game.FPS = 60
        self.window_surface = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        game.background = pygame.Surface(self.screen_size)
        game.background.fill(pygame.Color(self.bg_color))
        game.is_running = True
        game.clock = pygame.time.Clock()
        pygame.init()
        pygame.key.set_repeat(600, 75)
        pygame.display.set_caption('Not Wordle')
        game.manager = pygame_gui.UIManager(self.screen_size)
        game.texts = {}
        game.letters = {}
        game.rect = {}
        #game.color_rect = {}
        game.font = pygame.font.SysFont(self.general_font, 24)
        game.tick = 0
        game.started = False
        self.word = ""
        game.guess = []
        game.input_text = ""
        game.line = 0
        game.id = 0
        game.char_size = 150
        game.char_size_set = False
        game.full = False
        game.tick_tmp = 0
        game.win = False
        game.return_menu = False
    
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
        ft = pygame.font.SysFont(self.general_font, size)
        tx = ft.render(text, True, color)
        txt_size = ft.size(text)
        if centered:
            game.texts[str(id)]=(tx, (pos[0]*self.w-(txt_size[0]/2), pos[1]*self.h-(txt_size[1]/2)), txt_size)
        else:
            game.texts[str(id)]=(tx, (pos[0]*self.w, pos[1]*self.h))
        return str(id)

    def put_char(self, txt, idx):
        color = (255,255,255)
        ft = pygame.font.SysFont(self.general_font, game.char_size)
        txt_size = ft.size(txt)
        if not game.char_size_set:
            if txt_size[0]/self.w > game.rect[idx]['size'][0] or txt_size[1]/self.h > game.rect[idx]['size'][1]:
                while txt_size[0]/self.w > game.rect[idx]['size'][0] or txt_size[1]/self.h > game.rect[idx]['size'][1]:
                    game.char_size-=1
                    ft = pygame.font.SysFont(self.general_font, game.char_size)
                    txt_size = ft.size(txt)
            elif txt_size[1]/self.h < game.rect[idx]['size'][1]:
                while txt_size[1]/self.h < game.rect[idx]['size'][1]:
                    game.char_size+=1
                    ft = pygame.font.SysFont(self.general_font, game.char_size)
                    txt_size = ft.size(txt)
                game.char_size-=1
                ft = pygame.font.SysFont(self.general_font, game.char_size)
                txt_size = ft.size(txt)
            game.char_size_set = True
        tx = ft.render(txt, True, color)
        x= game.rect[idx]['pos'][0] + (txt_size[0]/2)/self.w
        y= game.rect[idx]['pos'][1] + game.rect[idx]['size'][1]/2
        game.id +=1
        game.letters[str(game.id)] = {'data':tx, 'pos':(x,y), 'size':txt_size, 'ref':idx, 'char': txt, 'line': idx.split()[0], 'column':idx.split()[1]}
        #print(game.id,">>", idx)
        return str(game.id)
    
    def convert_text(self,txt, line=0):
        i=0
        for letter in txt:
            idx = f"{line} {i}"
            self.put_char(letter.upper(), idx)
            i+=1
        return
    
    def start(self):
        self.button_play.kill()
        self.button_quit.kill()
        self.button_words.kill()
        l=[]
        with open("res/fr.txt", 'r') as f:
            for line in f:
                l.append(line.rstrip())
        self.word = random.choice(l)
        self.word.upper()
        l.clear()
        self.texts.clear() 
        #self.text((0.5, 0.1), self.word, 1, (0,200,0), 75)
        game.char_size_set=False
        self.game_ui()
        self.started = True

    def game_loop(self):
        i=0
        for wrd in game.guess:
            game.convert_text(self, wrd, i)
            i+=1
        for word in self.guess:
            if word == self.word:
                self.win = True
                self.full = True
        
    def draw_rect(self, id, pos, size, color=(50,50,50), keep_ratio = False):
        self.rect[str(id)] = {'pos':pos, 'size':size, 'color':color, 'ratio':keep_ratio, 'state':None, 'state_done': False}
        return str(id)

    def game_ui(self):
        box_size = 0.9/(len(self.word)*1.33)
        space_between = 0.01
        space_below = 0.02
        lines = len(self.word)
        y_offset = (0.5-(box_size*(lines+1)+space_below*(lines-1))/2)+0.02
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

    def update(self):
        self.screen_size = (self.window_surface.get_width(), self.window_surface.get_height())
        self.window_surface = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        pygame.draw.rect(self.window_surface, (20,20,20), (0,0,self.screen_size[0], self.screen_size[1]))
        game.manager = pygame_gui.UIManager(self.screen_size)
        if not self.started:
            for i in self.btn:
                i.kill()
            self.menu_btn()

    
    def refresh(self): 
        for rect in game.rect:
            if game.rect[rect]['ratio']:
                x= game.rect[rect]['pos'][0]*self.w - game.rect[rect]['size'][1]*self.h/2 ## centrer en x
                y= game.rect[rect]['pos'][1]*self.h - game.rect[rect]['size'][1]*self.h/2 ## centrer en y
                box = pygame.Rect(x, y, game.rect[rect]['size'][1]*self.h, game.rect[rect]['size'][1]*self.h)
            else:
                x= game.rect[rect]['pos'][0]*self.w - game.rect[rect]['size'][0]*self.w/2 ## centrer en x
                y= game.rect[rect]['pos'][1]*self.h - game.rect[rect]['size'][1]*self.h/2 ## centrer en y
                box = pygame.Rect(x, y, game.rect[rect]['size'][0]*self.w, game.rect[rect]['size'][1]*self.h)
            color = game.rect[rect]['color']
            if game.rect[rect]['state_done'] == False and game.rect[rect]['state'] != None:
                if not 'state_end' in game.rect[rect].keys():
                    game.rect[rect]['state_end'] = self.tick + game.FPS
                if game.rect[rect]['state'] == 1:
                    color1 = color[0] + ((game.color_good[0]-color[0]) * self.beizer(1-((game.rect[rect]['state_end']-self.tick)/game.FPS)))
                    color2 = color[1] + ((game.color_good[1]-color[1]) * self.beizer(1-((game.rect[rect]['state_end']-self.tick)/game.FPS)))
                    color3 = color[2] + ((game.color_good[2]-color[2]) * self.beizer(1-((game.rect[rect]['state_end']-self.tick)/game.FPS)))
                    color = (color1, color2, color3)
                elif game.rect[rect]['state'] == 2:
                    color1 = color[0] + ((game.color_almost[0]-color[0]) * self.beizer(1-((game.rect[rect]['state_end']-self.tick)/game.FPS)))
                    color2 = color[1] + ((game.color_almost[1]-color[1]) * self.beizer(1-((game.rect[rect]['state_end']-self.tick)/game.FPS)))
                    color3 = color[2] + ((game.color_almost[2]-color[2]) * self.beizer(1-((game.rect[rect]['state_end']-self.tick)/game.FPS)))
                    color = (color1, color2, color3)
                else:
                    color1 = color[0] + ((game.color_bad[0]-color[0]) * self.beizer(1-((game.rect[rect]['state_end']-self.tick)/game.FPS)))
                    color2 = color[1] + ((game.color_bad[1]-color[1]) * self.beizer(1-((game.rect[rect]['state_end']-self.tick)/game.FPS)))
                    color3 = color[2] + ((game.color_bad[2]-color[2]) * self.beizer(1-((game.rect[rect]['state_end']-self.tick)/game.FPS)))
                    color = (color1, color2, color3)
                if game.rect[rect]['state_end'] <= self.tick:
                    game.rect[rect]['color'] = color
                    game.rect[rect]['state_done'] = True
            pygame.draw.rect(self.window_surface, color, box)
        for txt in game.texts:
            self.window_surface.blit(game.texts[txt][0], game.texts[txt][1])
        for txt in game.letters:
            x= game.letters[txt]['pos'][0]*self.w - game.letters[txt]['size'][0] ## centrer en x
            y= game.letters[txt]['pos'][1]*self.h - game.letters[txt]['size'][1] ## centrer en y
            #pygame.draw.rect(self.window_surface, (200,0,0), pygame.Rect(x,y,game.letters[txt]['size'][0],game.letters[txt]['size'][1]))
            self.window_surface.blit(game.letters[txt]['data'], (x,y))
        if self.full:
            if self.tick_tmp == 0:
                self.tick_tmp = self.tick + 240
                if self.win:
                    self.text((0.5,0.98), "Tu as gagné !", "win")
                else:
                    self.text((0.5,0.98), "Le mot était: {}".format(self.word), "loose")
            if self.tick > self.tick_tmp:
                self.screenshot()
                self.full = False
                self.return_menu = True

    def display_fps(self):
        text_to_show = game.font.render(str(int(game.clock.get_fps())), True, (200,50,50))
        self.window_surface.blit(text_to_show, (5,5))

    def check_word(self):
        for text in game.letters:
            if game.letters[text]['line'] == str(self.line):
                if self.word[int(game.letters[text]['column'])].upper() == game.letters[text]['char']:
                    game.rect[game.letters[text]['ref']]['state'] = 1
                elif game.letters[text]['char'] in self.word.upper():
                    game.rect[game.letters[text]['ref']]['state'] = 2
                else:
                    game.rect[game.letters[text]['ref']]['state'] = 3
                
    def screenshot(self):
        now = datetime.now()
        path = "{}.jpg".format(now.strftime("%d/%m/%Y %H:%M:%S"))
        path = path.replace("/","-")
        path = path.replace(":", "-")
        pygame.image.save(self.window_surface, "screenshot/"+path)
    
    def reset(self):
        self.__init__()
        self.started = False
        self.full = False
        self.guess.clear()
        self.letters.clear()
        self.rect.clear()
        self.started = False
        self.word = ""
        self.input_text = ""
        self.line = 0
        self.char_size_set = False
        self.full = False
        self.tick_tmp = 0
        self.win = False
        self.return_menu = False

if __name__ == "__main__":
    print("Wrong file!\nTo play the game, launch the main.py file with:\u001b[32m\u001b[40;1m python3 main.py\u001b[0m")