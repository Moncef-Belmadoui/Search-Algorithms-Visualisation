from cell import Cell
import pygame
import sys 
from collections import deque
import random
import time
from  queue import PriorityQueue
import math
from settings import *


matrix = [[0 for _ in range(40)] for _ in range(40)]

def out_of_range(i,j):
    if i <= -1 or i >= 40:
        return True
    if j <= -1 or j >= 40:
        return True
    return False

def draw_padding(screen):
    for i in range(41):
        pygame.draw.line(screen, GREY, (0,i * CELL_HEIGHT), (WIDTH,i * CELL_HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen,GREY,(i * CELL_WIDTH,0),(i * CELL_WIDTH,HEIGHT),LINE_WIDTH)


def start_goal_position(screen,start_coord,goal_coord):
    x1,y1 = start_coord[0],start_coord[1]
    x2,y2 = goal_coord[0],goal_coord[1]
    matrix[x1][y1].change_color(YELLOW)
    matrix[x2][y2].change_color(PURPLE)


def create_grid(screen,start_coord,goal_coord):
    global matrix,ALREADY_CREATED
    for i in range(40):
        for j in range(40):
            matrix[i][j] = Cell(screen,i,j,CELL_WIDTH,CELL_HEIGHT,WHITE)
    start_goal_position(screen,start_coord,goal_coord)
    random_border()
    ALREADY_CREATED = True

def draw_grid(screen):
    global matrix
    for i in range(40):
        for j in range(40):
            matrix[i][j].draw_cell()
    draw_padding(screen)


def get_neighbors(i, j):
    neighbors = []
    if not out_of_range(i+1, j):
        if matrix[i+1][j].get_color() in {WHITE, PURPLE, LIGHT_BLUE}:
            neighbors.append((i+1, j))
    if not out_of_range(i-1, j):
        if matrix[i-1][j].get_color() in {WHITE, PURPLE, LIGHT_BLUE}:
            neighbors.append((i-1, j))
    if not out_of_range(i, j+1):
        if matrix[i][j+1].get_color() in {WHITE, PURPLE, LIGHT_BLUE}:
            neighbors.append((i, j+1))
    if not out_of_range(i, j-1):
        if matrix[i][j-1].get_color() in {WHITE, PURPLE, LIGHT_BLUE}:
            neighbors.append((i, j-1))
    return neighbors



def bfs(start,end):
    visited = set()       
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex) 
            if vertex != start:  
                matrix[vertex[0]][vertex[1]].change_color(RED)
            for neighbor in get_neighbors(vertex[0],vertex[1]):
                if neighbor not in visited and neighbor not in queue:
                    matrix[neighbor[0]][neighbor[1]].set_parent(vertex)
                    if neighbor == end:
                        neighbor = matrix[neighbor[0]][neighbor[1]].get_parent()
                        while neighbor != start:
                            matrix[neighbor[0]][neighbor[1]].change_color(GREEN)
                            neighbor = matrix[neighbor[0]][neighbor[1]].get_parent()
                            draw_grid(screen)
                            pygame.display.flip()
                        return True
                    queue.append(neighbor)
                    matrix[neighbor[0]][neighbor[1]].change_color(LIGHT_BLUE)
        draw_grid(screen)
        pygame.display.flip()

def A_star(start, end):
    count = 0
    frontier = PriorityQueue()
    start_cell = matrix[start[0]][start[1]]
    end_cell = matrix[end[0]][end[1]]
    frontier.put((0, count, start_cell))
    g_score = {spot: float("inf") for row in matrix for spot in row}
    g_score[start_cell] = 0
    f_score = {spot: float("inf") for row in matrix for spot in row}
    f_score[start_cell] = heuristic(start)

    frontier_hash = {start_cell}

    while not frontier.empty():
        current = frontier.get()[2]
        frontier_hash.remove(current)

        if current == end_cell:
            while current.get_parent()  != start_cell:
                current = current.get_parent()
                current.change_color(GREEN)  
                draw_grid(screen)
                pygame.display.flip()

            return True  

        if current != start_cell:
            current.change_color(RED)  

        for neighbor_coord in get_neighbors(current.x, current.y):
            neighbor_cell = matrix[neighbor_coord[0]][neighbor_coord[1]]
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor_cell]:
                neighbor_cell.set_parent(current)
                g_score[neighbor_cell] = temp_g_score
                f_score[neighbor_cell] = temp_g_score + heuristic(neighbor_coord)
                
                if neighbor_cell not in frontier_hash:
                    count += 1
                    frontier.put((f_score[neighbor_cell], count, neighbor_cell))
                    frontier_hash.add(neighbor_cell)

                    if neighbor_cell != end_cell:
                        neighbor_cell.change_color(LIGHT_BLUE)

        draw_grid(screen)
        pygame.display.flip()
    return False



def bidirctional(start , end):

    if start == end:
        return True

    visited_from_start = set()
    visited_from_end = set()

    frontier_from_start = deque([start])
    frontier_from_end = deque([end])

    while frontier_from_start and frontier_from_end:
        #expand from the start side
        if frontier_from_start:
            S_current = frontier_from_start.popleft()
            visited_from_start.add(S_current)
            if S_current !=start:
                matrix[S_current[0]][S_current[1]].change_color(RED)
            for neighbor in get_neighbors(S_current[0], S_current[1]):
                if neighbor not in visited_from_start and neighbor not in frontier_from_start:
                    if neighbor in visited_from_end or neighbor in frontier_from_end:
                        while neighbor != end:
                            matrix[neighbor[0]][neighbor[1]].change_color(GREEN)
                            neighbor = matrix[neighbor[0]][neighbor[1]].get_parent()
                            draw_grid(screen)
                            pygame.display.flip()
                        while S_current != start:
                            matrix[S_current[0]][S_current[1]].change_color(GREEN)
                            S_current = matrix[S_current[0]][S_current[1]].get_parent()
                            draw_grid(screen)
                            pygame.display.flip()
                        return True # return path
                    matrix[neighbor[0]][neighbor[1]].set_parent(S_current)
                    frontier_from_start.append(neighbor)
                    matrix[neighbor[0]][neighbor[1]].change_color(LIGHT_BLUE)

        #expand from the end 
        if frontier_from_end:
            E_current = frontier_from_end.popleft()
            visited_from_end.add(E_current)
            if E_current !=end:
                matrix[E_current[0]][E_current[1]].change_color(RED)
            for neighbor in get_neighbors(E_current[0], E_current[1]):
                if neighbor not in visited_from_end and neighbor not in frontier_from_end:
                    if neighbor in visited_from_start or neighbor in frontier_from_start:
                        while neighbor != start:
                            matrix[neighbor[0]][neighbor[1]].change_color(GREEN)
                            neighbor = matrix[neighbor[0]][neighbor[1]].get_parent()
                            draw_grid(screen)
                            pygame.display.flip()
                        while E_current != end:
                            matrix[E_current[0]][E_current[1]].change_color(GREEN)
                            E_current = matrix[E_current[0]][E_current[1]].get_parent()
                            draw_grid(screen)
                            pygame.display.flip()
                        return True # return path
                    matrix[neighbor[0]][neighbor[1]].set_parent(E_current)
                    frontier_from_end.append(neighbor)
                    matrix[neighbor[0]][neighbor[1]].change_color(LIGHT_BLUE)
        draw_grid(screen)
        pygame.display.flip()


def heuristic(p1,p2=GOAL_POS):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def random_border():
    for i in range(40):
        for j in range(40):
            x = random.randint(0,10)
            if x >7:
                if matrix[i][j].get_color() == WHITE:
                    matrix[i][j].change_color(BLACK)

#================================ 

ALREADY_CREATED = False
right_dragging = False
left_dragging = False



pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Search Algorithms Visualisation')


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  #left mouse button
                left_dragging = True
            if event.button == 3: # right mouse button
                right_dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                left_dragging = False
            if event.button == 3: 
                right_dragging = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # press the space bar to run the algorithm
                if STRATEGY==1:
                    A_star(STARTING_POS,GOAL_POS)
                elif STRATEGY==2:
                    bidirctional(STARTING_POS,GOAL_POS)
                elif STRATEGY==3:
                    bfs(STARTING_POS,GOAL_POS)

    screen.fill((255, 255, 255))

    if not ALREADY_CREATED:
        create_grid(screen,STARTING_POS,GOAL_POS)

    mouseX , mouseY = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
    if left_dragging:
        if not out_of_range(mouseX // CELL_HEIGHT,mouseY // CELL_WIDTH):
            if matrix[mouseX // CELL_HEIGHT][mouseY // CELL_WIDTH].get_color() == WHITE and mouseX >= 0   and mouseY >= 0:
                matrix[mouseX // CELL_HEIGHT][mouseY // CELL_WIDTH].change_color(BLACK)
    
    if right_dragging:
        if not out_of_range(mouseX // CELL_HEIGHT,mouseY // CELL_WIDTH):
            if matrix[mouseX // CELL_HEIGHT][mouseY // CELL_WIDTH].get_color() == BLACK and mouseX >= 0   and mouseY >= 0:
                matrix[mouseX // CELL_HEIGHT][mouseY // CELL_WIDTH].change_color(WHITE)

    

    draw_grid(screen)
    pygame.display.flip()


pygame.quit()
sys.exit()

