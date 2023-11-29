import pygame
import time
from boggle import *

class Button:
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None, border_radius=0):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),border_radius)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),border_radius)
        
        if self.text != '':
            font = pygame.font.SysFont('Arial', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
    
class GameTileButton(Button):
    def __init__(self, color, x, y, width, height, text=''):
        super().__init__(color, x, y, width, height, text)
        self.used = False
        self.width = 100
        self.height = 100
        self.selectedColor = (255,100,0) #orange
        self.unselectedColor = (255,255,255)
        self.hoverColor = (225,125,125)
        self.stateColor = self.unselectedColor
        self.prevStateTime = 0
    
    def change_state(self):
        if self.used:
            self.used = False
            self.stateColor = self.unselectedColor
            self.color = self.stateColor
        else:
            self.used = True
            self.stateColor = self.selectedColor
            self.color = self.stateColor
    
    def __repr__(self):
        return self.text
                        
class Game():
    def __init__(self):
    # def set_up():
        pygame.init()

        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 700

        self.time_limit = 30
        self.isOpen = True
        self.useKeyboard = True
        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        ### SET LOADING SCREEN HERE
        self.SCREEN.fill((100,100,255))
        self.loading_msg = Button((100,100,255), 250, 250, 500, 200, "Loading")
        self.loading_msg.draw(self.SCREEN)
        pygame.display.set_caption("Boggle")
        pygame.display.update()

        self.text_box = []

        self.gameSession = Session()

        # make this gui board set up into a fnction for game class
        # then can also have self.real_board which is board class import from prev file
        # then when make a new game, do real board shuffle, then update gui board
        self.gui_board = [[None]*4 for _ in range(self.gameSession.board.size)]
        # print(self.gui_board)
        # self.test_board = self.gameSession.board.board
        self.make_gui_board()

        # member (state) variables for navigation between main menu game screen & end game screen, dont want to have a bunch of hanging functions
        self.inGame = False
        self.inAfterGame = False

    def make_gui_board(self):
        gx, gy = 0, 0
        for i in range(400,self.SCREEN_WIDTH - 100, (self.SCREEN_WIDTH-500) // 4):
            gx = 0
            for j in range(100, self.SCREEN_HEIGHT - 100, (self.SCREEN_HEIGHT-200)//4):
                self.gui_board[gx][gy] = GameTileButton((255,255,255), i, j, 100, 100, self.gameSession.board.board[gx][gy])
                gx += 1
            gy += 1

        # print(self.gui_board)
    
    def disp_gui_board(self):
        for r in range(len(self.gui_board)):
            for c in range(len(self.gui_board[r])):
                self.gui_board[r][c].draw(self.SCREEN, (0,0,0))
        
    def game_loop(self):
        # Game set up:
        score = 0

        self.gameSession.board.solution_set.clear()
        self.gameSession.board.shuffle()
        self.gameSession.board.solve_board(self.gameSession.dictionary)
        print(self.gameSession.board.solution_set)
        self.make_gui_board()

        start_time = time.time()
        running = True

        for i in range(len(self.gui_board)):
            for j in range(len(self.gui_board[i])):
                self.gui_board[i][j].prevStateTime = 0

        lastTimeDispUpdate = 0

        #start game/event handler loop
        while running:
            elapsed_time = time.time() - start_time
            if elapsed_time > self.time_limit:
                print(30)
                running = False
                continue
            if elapsed_time >= 1 + lastTimeDispUpdate:
                print(int(elapsed_time))
                lastTimeDispUpdate = elapsed_time

            self.SCREEN.fill((100,100,255))

            #draw board background
            pygame.draw.rect(self.SCREEN, (255,174,66), (375,75,525,525))
            
            #draw letter tiles
            self.disp_gui_board()

            pygame.display.update()

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    self.isOpen = False
                    break

                # mouse clicks for buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.useKeyboard:
                        for i in range(len(self.gui_board)):
                            for j in range(len(self.gui_board[i])):
                                if self.gui_board[i][j].isOver(pos):
                                    print("button clicked")
                                    # if not self.gui_board[i][j].used:
                                    #     self.text_box.append(self.gui_board[i][j].text)
                                    #     print("curr string: " + "".join(self.text_box))

                                    self.gui_board[i][j].change_state()
                                    self.gui_board[i][j].prevStateTime = elapsed_time
                                    # add call backs for either appending letter or submitting current word

                    #check for options button (to switch self.useKeyboard), will always be active:

                if not self.useKeyboard:
                    # MOUSE HOVERS (for buttons)
                    if event.type == pygame.MOUSEMOTION:
                        for i in range(len(self.gui_board)):
                            for j in range(len(self.gui_board[i])):
                                if self.gui_board[i][j].isOver(pos) and not self.gui_board[i][j].used and (elapsed_time - self.gui_board[i][j].prevStateTime) > 0.5:
                                    self.gui_board[i][j].color = self.gui_board[i][j].hoverColor
                                else:
                                    self.gui_board[i][j].color = self.gui_board[i][j].stateColor
                
                # keyboard typing events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE and self.useKeyboard:
                        self.text_box.pop()


                    elif event.key == pygame.K_RETURN and self.useKeyboard:
                        #guess word
                        print("Guessed: " + "".join(self.text_box))
                        isWord = self.gameSession.board.check_word_guess("".join(self.text_box))
                        if isWord:
                            print("is a word")
                            score += len(self.text_box)
                        else:
                            print("not a word")
                        self.text_box = []

                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    
                    elif len(self.text_box) < 16 and self.useKeyboard:
                        if event.key == pygame.K_a:
                            self.text_box.append("A")
                        elif event.key == pygame.K_b:
                            self.text_box.append("B")
                        elif event.key == pygame.K_c:
                            self.text_box.append("C")
                        elif event.key == pygame.K_d:
                            self.text_box.append("D")
                        elif event.key == pygame.K_e:
                            self.text_box.append("E")
                        elif event.key == pygame.K_f:
                            self.text_box.append("F")
                        elif event.key == pygame.K_g:
                            self.text_box.append("G")
                        elif event.key == pygame.K_h:
                            self.text_box.append("H")
                        elif event.key == pygame.K_i:
                            self.text_box.append("I")
                        elif event.key == pygame.K_j:
                            self.text_box.append("J")
                        elif event.key == pygame.K_k:
                            self.text_box.append("K")
                        elif event.key == pygame.K_l:
                            self.text_box.append("L")
                        elif event.key == pygame.K_m:
                            self.text_box.append("M")
                        elif event.key == pygame.K_n:
                            self.text_box.append("N")
                        elif event.key == pygame.K_o:
                            self.text_box.append("O")
                        elif event.key == pygame.K_p:
                            self.text_box.append("P")
                        elif event.key == pygame.K_q:
                            self.text_box.append("Q")
                        elif event.key == pygame.K_r:
                            self.text_box.append("R")
                        elif event.key == pygame.K_s:
                            self.text_box.append("S")
                        elif event.key == pygame.K_t:
                            self.text_box.append("T")
                        elif event.key == pygame.K_u:
                            self.text_box.append("U")
                        elif event.key == pygame.K_v:
                            self.text_box.append("V")
                        elif event.key == pygame.K_w:
                            self.text_box.append("W")
                        elif event.key == pygame.K_x:
                            self.text_box.append("X")
                        elif event.key == pygame.K_y:
                            self.text_box.append("Y")
                        elif event.key == pygame.K_z:
                            self.text_box.append("Z")
                    else:
                        print("guess too long already")    


                    print("curr string: " + "".join(self.text_box))

        # once have end screen and/or menu set up, will go there instead of quiting pygame
        print(score)
        # pygame.quit()
        self.inGame = False
        self.inAfterGame = True
        return score    

    def main_menu(self):
        print("main menu")
        running = True
        playButton = Button((255,255,255), 250, 250, 500, 200, "Play")
        start_time = time.time()
        newGame = False

        while running:
            elapsed_time = time.time() - start_time

            if self.inGame:
                # score, outputs, etc (need these as member vars?) = self.game_loop
                score = self.game_loop()
            
            if self.inAfterGame:
                newGame = self.after_game(score)
                # when done set after game to False
                # #how to handle play another game?
                # # set inGame to True again?

            if newGame:
                self.inGame = True
                continue
            
            if not self.isOpen:
                running = False
                pygame.quit()
                break
            # disp menu:
            self.SCREEN.fill((100,100,255))

            # disp buttons:
            playButton.draw(self.SCREEN)
            
            # update screen:
            pygame.display.update()

            # event handler
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    break

                # mouse clicks for buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playButton.isOver(pos):
                        print("play button clicked")
                        self.inGame = True

        return

    def after_game(self, score):
        # can pass more stuff in here later if need to display certain game info after the current game ends
        # print("after game screen")
        # print("Previous Score: " + str(score))
        scoreStr = "Previous Score: " + str(score)

        running = True
        playButton = Button((255,255,255), 250, 300, 500, 100, "Play Again")
        mainMenuButton = Button((255,255,255), 250, 500, 500, 100, "Main Menu")
        prevScore = Button((255,255,255), 250, 100, 500, 100, scoreStr)

        while running:
            # disp menu:
            self.SCREEN.fill((100,100,255))

            # disp buttons:
            playButton.draw(self.SCREEN)
            mainMenuButton.draw(self.SCREEN)
            prevScore.draw(self.SCREEN)

            # update screen:
            pygame.display.update()

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    self.isOpen = False
                    break

                # mouse clicks for buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playButton.isOver(pos):
                        print("play button clicked")
                        self.inAfterGame = False
                        return True
                    
                    if mainMenuButton.isOver(pos):
                        print("main menu clicked")
                        self.inAfterGame = False
                        return False


        self.inAfterGame = False
        return False

if __name__ == "__main__":
    g = Game()
    # g.game_loop()
    g.main_menu()