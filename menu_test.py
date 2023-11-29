import pygame
from gui import *

class BoggleGUI():

    def __init__(self):
        pygame.init()
        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 700
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        ### SET LOADING SCREEN HERE
        self.SCREEN.fill((50,50,255))

        pygame.display.set_caption("Boggle")

    def main_menu(self):
        while True:
            # self.SCREEN.blit(BG, (0, 0))

            # MENU_MOUSE_POS = pygame.mouse.get_pos()

            # PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
            #                     text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            # OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
            #                     text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            # QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
            #                     text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.SCREEN.fill((50,50,255))
            self.loading_msg = Button((255,255,255), 250, 250, 500, 200, "Loading")
            self.loading_msg.draw(self.SCREEN)
            # for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            #     button.changeColor(MENU_MOUSE_POS)
            #     button.update(self.SCREEN)
            
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         sys.exit()
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         continue
                    # if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #     play()
                    # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #     options()
                    # if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #     pygame.quit()
                    #     sys.exit()

            pygame.display.update()

    def options(self):
        return

    def play_game(self):
        #main game loop here
        return

    def after_game(self, score):
        #end game screen here, will take in previous game score to display results here
        #can also add in list of words guessed/"screenshot" of the board here later to have more info to review prev. game played
        return


if __name__ == "__main__":
    g = BoggleGUI()
    g.main_menu()