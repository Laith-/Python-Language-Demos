from pygameframework import Window
import time
import pygame
from pygame.locals import *
import random

def main():
    window = Window('memory3', 500, 400)
    game = Game(window)
    game.play()
    window.close()

class Game:
    selected = []
    def __init__(self, window):
        self.window = window
        Tile.set_window(window) # call to the class method in Tile
        self.pause_time = 0.04 # smaller is faster game
        self.close_clicked = False
        self.continue_game = True
        
        self.images = []
        self.board = []
        self.import_image()
        self.create_board()
        self.score = 0
        self.tile_count = 0
        
    def import_image(self):
        for i in range(1,9):
            path = 'image'+str(i)+'.bmp'
            image_temp = pygame.image.load(path)
            self.images.append(image_temp)
            self.images.append(image_temp)
        random.shuffle(self.images)
        
    def create_board(self):
        self.tile_count = 0
        for row_index in range(4):
            row=self.create_row(row_index)
            self.board.append(row)
            
    def create_row(self,row_index):
        row= []
        width = self.window.get_width()//5
        height = self.window.get_height()//4
        for i in range(4):
            x = width * i
            y = height * row_index
            tile = Tile(x,y,width,height,self.images[self.tile_count])
            row.append(tile)
            self.tile_count = self.tile_count + 1
        return row
    
    def play(self):
        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_event()
            self.draw()
            self.compare()
            if self.continue_game:
                self.update()
                self.decide_continue()
            time.sleep(self.pause_time) # set game velocity by pausing
                       
    def handle_event(self):
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        if event.type == MOUSEBUTTONUP and self.continue_game:
            self.handle_mouse_up(event.pos)
            
    def handle_mouse_up(self,position):
        for row in self.board:
            for tile in row:
                counted = tile.select(position)
                    
    def draw(self):
        self.window.clear()
        self.draw_score()
        for row in self.board :
            for tile in row:
                tile.draw()
        self.window.update()
        
    def draw_score(self):
        self.window.set_font_size(70)
        score_string = str(self.score)
        string_len = self.window.get_string_width(score_string)
        self.window.draw_string(score_string,500-string_len,0)
    
    def update(self):
        self.score = pygame.time.get_ticks()//1000  
        
    def decide_continue(self):
        #fancy nested for loop
        #if all(tile.clicked == True for row in range(len(self.board)) for tile in self.board[row]):
            #self.continue_game = False
        
        win = 0
        for i in self.board:
            for row in i:
                if row.clicked == True:
                    win += 1
        if win == 16:
            self.continue_game = False
            
    def compare(self):
        if len(Game.selected) == 2:
            if Game.selected[0] != Game.selected[1]:
                time.sleep(.2)
                for tile in Game.selected:
                    tile.clicked = False
            else:
                for tile in Game.selected:
                    tile.clicked = True
            Game.selected = []
        
class Tile:
    # class attributes
    fg_color = 'black'
    border_size = 3
    window = None
    @classmethod
    def set_window(cls,window_from_Game):
        cls.window = window_from_Game
        
    #Instance MEthods
    def __init__(self,x,y,width,height,image,):
        # Instance Attributes
        self.rect = pygame.Rect(x,y,width,height)
        self.clicked = False
        self.image = image
        self.question_mark = pygame.image.load('image0.bmp')
        
    def __eq__(self,other_tile):
        return self.image == other_tile.image
        
    def draw(self):
        surface = Tile.window.get_surface()
        if not self.clicked:
            surface.blit(self.question_mark,self.rect)
        else:
            surface.blit(self.image,self.rect)
        pygame.draw.rect(surface,pygame.Color(Tile.fg_color),self.rect,Tile.border_size)
            
    def select(self,position):
        if self.rect.collidepoint(position) and not self.clicked:         
            self.clicked = True
            Game.selected.append(self) 
                
main()
