import pygame
from settings import *
class Cell:
    def __init__(self,screen,x,y,width,height,color ,parent =None):
        self.screen=screen
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.parent = parent
        

 

    def set_parent(self,p):
        self.parent = p

    def get_parent(self):
        return self.parent

    def get_color(self):
        return self.color

    def change_color(self,color):
        self.color = color

    def get_coord(self):
        return (self.x,self.y)
    def draw_cell(self):
        pygame.draw.rect(self.screen, self.color, (self.x * 20 , self.y * 20 , CELL_WIDTH, CELL_HEIGHT))

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
