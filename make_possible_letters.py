import csv
import os

def main():
    f = open('english_classic_boggle.csv', 'r')
    reader = csv.reader(f)
    letters = []

    for row in reader:
        letters.append(row)

    print(letters)
    # print(len(letters[6][4])) if letter len == 2, then its Q + u and need to account for this in if it is word (and scoring??)

#make function where you give/select language/game version, and then it generates the possible letters list for that selection
# then use other function in boggle.py to make the letter dice objects/list of objects
# can then use this + rand nums to generate boards to play

if __name__ == '__main__':
    main()