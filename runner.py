from os import kill
import sys, pygame, sample
from pygame.locals import *

LINE_LENGTH = 40
NUM_LINES = 3
FONT_SIZE_HEIGHT = 40
FONT_SIZE = FONT_SIZE_HEIGHT
FONT_SIZE_WIDTH = 25
OFFSET = 100

class Letter():
    def __init__(self, letter, index, x, y):
        self.letter = letter
        self.index = index
        self.x = x
        self.y = y
        self.cursor_on = False
        self.cursor_passed = False

class Paragraph():
    def __init__(self, sample_list, last_end):
        self.letters = []
        ind = 0
        x, y = 0, 0
        self.end_word = -1
        for index, word in enumerate(sample_list):
            if index <= last_end:
                continue
            if len(word) > LINE_LENGTH*NUM_LINES - ind - 1:
                self.end_word = index
                break
            if len(word) > LINE_LENGTH - x:
                x = 0
                y += 1
            for letter in word:
                self.letters.append(Letter(letter, ind, x, y))
                ind += 1
                x += 1
            self.letters.append(Letter(" ", ind, x, y))
            ind+=1
            x += 1
        self.letters[0].cursor_on = True

    def getLetter(self,index):
        return self.letters[index].letter

    def moveCursor(self, index):
        for i in range(len(self.letters)):
            self.letters[i].cursor_on = False
        self.letters[index].cursor_on = True
        self.letters[index-1].cursor_passed = True

    def reachedEnd(self, index):
        return (index+1) not in range(len(self.letters))


pygame.init()

size = width, height = 1200, 800

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Runner')
font = pygame.font.Font('font/AnonymousPro-Regular.ttf', FONT_SIZE)
set_sample = sample.sample()
paragraph = Paragraph(set_sample, -1)
last_end = paragraph.end_word

cursor_location = 0

running = True
while(running):

    screen.fill(pygame.Color("white"))
    
    for l in paragraph.letters:
        color_c = (0,0,0)
        let = l.letter
        if l.cursor_on:
            color_c = pygame.Color("red")
            if let == " ":
                let = "_"
        elif l.cursor_passed:
            color_c = pygame.Color("gray")
        else:
            color_c = pygame.Color("black")
        text = font.render(let, True, color_c)
        text_rect = text.get_rect(center=(l.x*FONT_SIZE_WIDTH+OFFSET, l.y*FONT_SIZE_HEIGHT+OFFSET))
        screen.blit(text, text_rect)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if chr(event.key) == paragraph.getLetter(cursor_location):
                #move cursor
                if paragraph.reachedEnd(cursor_location):
                    # create new paragraph
                    paragraph = Paragraph(set_sample, last_end)
                    last_end = paragraph.end_word
                    cursor_location = 0
                else:
                    cursor_location += 1
                    paragraph.moveCursor(cursor_location)
    
