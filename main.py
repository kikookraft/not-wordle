## Written in python 3.8.5 with pygame 2.1.2 (SDL 2.0.18)

# --- BUGS ---
# - Problèmes de redimensionement (linux, pygame 2.1.2 && python 3.8.10)
# TODO Dessiner flèche pour indiquer la ligne éditable
# TODO Empecher plusieures mêmes lettres d'avoir les couleurs
# TODO Créer système pour ne pas avoir 2 fois le même mot
#      (y faire avec un fichier texte)
# TODO Le menu pour voir les mots
# TODO Le bouton permettant de suprimmer les mots inconnus

import pygame #2.1.2
import pygame_gui #0.6.4
from game import game

if __name__ == "__main__":
    G = game()
    G.menu_btn()
    G.update()
    G.button_words.disable()
    kik = G.text((0.01,0.95), "By kikookraft", 0, centered=False)
    title = G.text((0.5,0.1), "Definitely not Wordle", 1, size=50)

    while G.is_running:
        time_delta = G.clock.tick(G.FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                G.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    G.return_menu = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if G.started:
                    if event.key == pygame.K_BACKSPACE:
                        if len(G.input_text)>0:
                            G.input_text = G.input_text[:-1]
                            G.update()
                            G.letters.clear()
                            G.convert_text(G.input_text,G.line)
                            G.game_loop()
                    elif event.key == pygame.K_RETURN:
                        if len(G.input_text)==len(G.word) and not G.full:
                            G.check_word()
                            G.update()
                            G.letters.clear()
                            G.convert_text(G.input_text,G.line)
                            G.guess.append(G.input_text)
                            G.input_text=""
                            G.line+=1
                        else:
                            print("Texte trop court")
                        G.game_loop()
                    elif len(G.input_text)<len(G.word) and event.unicode in "abcdefghijklmnopqrstuvwxyz" and not G.full:
                        G.update()
                        G.letters.clear()
                        G.input_text += event.unicode
                        G.convert_text(G.input_text,G.line)
                        G.game_loop()
                if G.line >= len(G.word)+1:
                    G.full = True
                    
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
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
                G.letters.clear()
                G.refresh()
                G.update()
                G.button_words.disable()
                G.rect.clear()
                if G.started:
                    G.game_ui()
                    G.convert_text(G.input_text,G.line)
                    G.game_loop()
                try:del G.texts[kik]
                except:pass
            G.manager.process_events(event)
        if G.return_menu:
            G.reset()
            G.update()
            G.button_words.disable()
            kik = G.text((0.01,0.95), "By kikookraft", 0, centered=False)
            title = G.text((0.5,0.1), "Definitely not Wordle", 1, size=50)
        G.manager.update(time_delta)
        G.window_surface.blit(G.background, (0, 0))
        G.manager.draw_ui(G.window_surface)
        G.refresh()
        G.display_fps()
        pygame.display.update()
        G.tick += 1
