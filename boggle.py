import csv
import random
# import enchant
import time
import os
import pickle

class letter_die:
    def __init__(self, possible_letters = None):
        if possible_letters is None:
            self.possible_letters = []
        self.possible_letters = possible_letters
        self.current_letter = None

    def set_possible_letters(self, letters):
        self.possible_letters = []

        for i in range(len(letters)):
            self.possible_letters.append(letters[i])

    def set_current_letter(self, letter_index):
        if letter_index < len(self.possible_letters):
            self.current_letter = self.possible_letters[letter_index]
        else:
            print("index out large, not enough possible letters")

    def __repr__(self):
        error_msg = "current_letter is not set"

        if self.current_letter:
            return self.current_letter
        else:
            return error_msg

class GameBoard:
    def __init__(self, size):
        self.size = size
        self.dice = self.tile_set_up(self.size)
        self.board = self.board_set_up(self.dice, self.size)# is 2d grid of self.size x self.size
        self.letterPositions = {}
        self.neighbors = {}

        # self.dictionary = enchant.Dict("en_US")
        self.solution_set = set()

        self.set_letter_positions()
        self.set_neighbors()
        #self.solve_board()
        #print(self)

    def shuffle(self):
        self.dice = self.tile_set_up(self.size)
        self.board = self.board_set_up(self.dice, self.size)
        #print(self)

    def tile_set_up(self, board_size):
        letter_dice = []

        f = open('english_classic_boggle.csv', 'r')
        reader = csv.reader(f)
        possible_letters = []

        for row in reader:
            possible_letters.append(row)

        for i in range(board_size ** 2):
            die = letter_die(possible_letters[i])
            letter_dice.append(die)


        return letter_dice

    def board_set_up(self, dice, board_size):
        board = []

        for die in dice:
            die.set_current_letter(random.randint(0,5))
            # print(die)

        for i in range(board_size):
            board.append([])
            for j in range(board_size):
                index = i*4 + j
                board[i].append(dice[index].current_letter)

        return board
    
    def __repr__(self):
        return '\n---------------------\n'.join([' | '.join(" Qu" if c =='QU' else " " + str(c) + " " for c in row) for row in self.board])
    
    def set_letter_positions(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] in self.letterPositions:
                    self.letterPositions[self.board[i][j].upper()].append((i*4 + j))
                else:
                    self.letterPositions[self.board[i][j].upper()] = [(i*4 + j)]
        # print(self.letterPositions)
    
    def set_neighbors(self):
        for i in range(self.size**2):

            checks = [i-5, i-4, i-3, i-1, i+1, i+3, i+4, i+5]
            i_right = [7,4,2]
            i_left = [5,3,0]

            if (i+1)%4 == 0:
                for k in range(len(i_right)):
                    del checks[i_right[k]]
            if (i)%4 == 0:
                for k in range(len(i_left)):
                    del checks[i_left[k]]

            for j in range(len(checks)):
                if 0 <= checks[j] <= 15:
                    self.neighbors.setdefault(i, []).append(checks[j])
        # print(self.neighbors)

    def check_word_guess(self, guess):
        if guess in self.solution_set:
            return True
        else:
            return False
        # def check(word):
        #     word = word.upper()
        #     wordList = []
        #     quFlag = False
            
        #     for idx, c in enumerate(word):
        #         curr = ""
        #         if c == "Q":
        #             if idx >= len(word) -1:
        #                 quFlag = True
        #                 #print("q at end (w/o u)")
        #             curr += "QU"
        #             wordList.append(curr)
        #             continue
        #         if idx > 0 and word[idx-1] == "Q":
        #             if c != 'U':
        #                 #print("q without u following")
        #                 quFlag = True
        #         if c == "U":
        #             if idx >0 and word[idx-1] == "Q":
        #                 continue
        #         curr += c
        #         wordList.append(curr)
            
        #     #print(wordList)
        #     if quFlag:
        #         #print("quFlag")
        #         return False
            
        #     #print(letter_positions2)
        #     if wordList[0] not in self.letterPositions:
        #         #print("first letter not present")
        #         return False

        #     is_used = {}

        #     ## make this into reset is_used dict function?
        #     for i in range(self.size**2):
        #         is_used[i] = False

        #     def dfs(curPos, i):
        #         #base cases: wl[i] is not in board, wl[i] is already used, i is out of bounds(end of word/full word found)
        #         # print("curPos: " + str(curPos) + ", cur index i: " + str(i))
        #         if i >= len(wordList):
        #             return 1
        #         if is_used[curPos]:
        #             # print("letter position already used")
        #             return 0 
        #         if wordList[i] not in self.letterPositions:
        #             return 0

        #         #use position
        #         is_used[curPos] = True

        #         res = 0
        #         for n in self.neighbors[curPos]:
        #             res = max(res, dfs(n, i+1))
        #             # print("res: " + str(res))
        #         return res
            
        #     #need to call for each instance of wordlist[0] in board
        #     ans = 0

        #     for start in self.letterPositions[wordList[0]]:
        #         ans = dfs(start, 0)
        #         if ans == 1:
        #             break
        #     return ans

        # inBoard = False
        # if len(guess) <= 2 or len(guess) > 16:
        #     return inBoard
        # else:
        #     inBoard = check(guess)
        
        # if inBoard and self.dictionary.check(guess):
        #     return True
        # else:
        #     return False

    def solve_board(self, preFixTrie):
        visited = set()
        directions = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]

        def dfs(i, j, curPath):
            if i < 0 or i >= len(self.board) or j < 0 or j >= len(self.board):
                return
            if (i, j) in visited:
                return
            curString = "".join(curPath)
            # print(curPath)
            # print(type(curString))
            # print(curString)
            if not preFixTrie.startsWith(curString):
                return
            #add a check here w/Trie so that can cut off calls that won't ever result in a word

            ####### MAKE CURR PATH A LIST OF TUPLES WITH THE I,J POSITION OF EACH LETTER, THEN MAKE A VARIABLE WITH CURRSTRING, WHICH HAS THE CURRENT LETTER STRING
            ####### THIS WAY CAN HAVE THE PATH SO WHEN DISPLAYING ANSWERS LATER, CAN DISPLAY THE ANSWER PATH WHEN ANSWER WORD IS CLICKED

            curPath.append(self.board[i][j])
            #if curPath is a word in trie dict, then add to results
            if preFixTrie.search(curString) and len(curString) > 2:
                #need to add string, prev add argument: tuple(curPath.copy())
                self.solution_set.add(curString)
            visited.add((i,j))

            for dy, dx in directions:
                dfs(i+dy, j+dx, curPath)
            if len(curPath) > 0:
                curPath.pop()
            if (i,j) in visited:
                visited.remove((i,j))
            return
        # for i in range(4):
        #     for j in range(4):
        #         dfs(i,j,[])
        for i in range(4):
            for j in range(4):
                dfs(i,j,[])
                    
        return

class TrieNode():
    def __init__(self):
        self.children = {}
        self.isWord = False

class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            #add letter
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.isWord = True
            
    def search(self, word: str) -> bool:
        curr = self.root
        for c in word:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        if curr.isWord == True:
            return True
        return False

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return True
    
class Session():
    def __init__(self):
        with open('preFixTrie.pickle','rb') as f:
            self.dictionary = pickle.load(f)
        self.board = GameBoard(4)

        ## code used to create prefixtrie and save to pickled file, this will be loaded and used as self.dictionary
        # f = open("words_alpha.txt","r")
        # all_words_list = f.read().splitlines()
        # # all_words_set = set(all_words_list)
        # preFixTrie = Trie()
        # for w in all_words_list:
        #     preFixTrie.insert(w.upper())
        
        # with open('preFixTrie.pickle', 'wb') as f:
        #     pickle.dump(preFixTrie, f)
    
    def startGame(self):
        self.board.solution_set.clear()
        self.board.shuffle()
        self.board.solve_board(self.dictionary)
        print(self.board)

        print("game started")
        score = 0
        # time_limit = 5
        guess_limit = 3
        guesses = 0

        # start_time = time.time()
        while True:
            # elapsed_time = time.time() - start_time
            # if elapsed_time >= time_limit:
            #     break
            if guesses >= guess_limit:
                break
            w = input("enter word: ").upper()
            guesses += 1
            guessResult = self.board.check_word_guess(w)
            
            if guessResult:
                print("is a word")
                score += len(w)
            print("score: " + str(score))

        # dictionary = enchant.Dict("en_US")
        # print(check_guess(w))
        # guessResult = dictionary.check(w)
        print("all guesses used, game is over")
        print("final score: " + str(score))

        return

def main():
    #board = GameBoard(4)
    game = Session()
    print("game and dict loaded")

    game.startGame()

    while 1:
        response = input("Play another game? (y/n): ")
        if response == 'y':
            game.startGame()
        else:
            break
    return

if __name__ == "__main__":
    main()