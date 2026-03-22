# /ᐠ｡ꞈ｡ᐟ\

import pygame, sys, time
from pygame.locals import *  # pyright: ignore[reportWildcardImportFromLibrary]

class Cell():
    grid = []
    def __init__(self,ig_pos:tuple[int,int],state:bool=False)->None:
        self.__ig_pos = ig_pos
        self.__state = state
        self.__next_state = False
        
        Cell.grid.append(self)
        if state:
            for x in range(ig_pos[0]-1,ig_pos[0]+2):
                for y in range(ig_pos[1]-1,ig_pos[1]+2):
                    if check_grid((x,y)) is None:
                        Cell((x,y))
        """neighnours = [False,False,False,False,False,False,False,False]
            for cell in Cell.grid:
                if cell.get_pos() == (ig_pos[0]-1,ig_pos[1]-1):
                    neighnours[0] = True
                elif cell.get_pos() == (ig_pos[0],ig_pos[1]-1):
                    neighnours[1] = True
                elif cell.get_pos() == (ig_pos[0]+1,ig_pos[1]-1):
                    neighnours[2] = True
                elif cell.get_pos() == (ig_pos[0]-1,ig_pos[1]):
                    neighnours[3] = True
                elif cell.get_pos() == (ig_pos[0]+1,ig_pos[1]):
                    neighnours[4] = True
                elif cell.get_pos() == (ig_pos[0]-1,ig_pos[1]+1):
                    neighnours[5] = True
                elif cell.get_pos() == (ig_pos[0],ig_pos[1]+1):
                    neighnours[6] = True
                elif cell.get_pos() == (ig_pos[0]+1,ig_pos[1]+1):
                    neighnours[7] = True"""
        
        return
    def get_pos(self)->tuple[int,int]:# in game pos
        return self.__ig_pos
    def get_state(self)->bool:
        return self.__state
    def get_next_state(self)->bool:
        return self.__next_state
    def set_next_state(self,state:bool)->None:
        self.__next_state = state
        return
    def set_state(self,state:bool)->None:
        self.__state = state
        return
    def change_state(self)->None:
        if self.__state == True:
            self.__state = False
        else:
            self.__state = True
            for x in range(self.__ig_pos[0]-1,self.__ig_pos[0]+2):
                for y in range(self.__ig_pos[1]-1,self.__ig_pos[1]+2):
                    if check_grid((x,y)) is None:
                        Cell((x,y))
        return

def place_cell(mouse_pos:tuple[int,int])->None:
    Cell(convert_mouse_pos(mouse_pos),True)
    return

def draw_cell(cell:Cell):#->RectValue:
    cell_pos = convert_ig_pos(cell.get_pos())
    return(cell_pos[0],cell_pos[1],size,size)

def convert_mouse_pos(mouse_pos:tuple[int,int])->tuple[int,int]:
    win_size = pygame.display.get_window_size()
    return (mouse_pos[0]-win_size[0]//2)//size,(mouse_pos[1]-win_size[1]//2)//size

def convert_ig_pos(ig_pos:tuple[int,int])->tuple[int,int]:
    win_size = pygame.display.get_window_size()
    return ig_pos[0]*size+win_size[0]//2,ig_pos[1]*size+win_size[1]//2

def check_grid(ig_pos:tuple[int,int])->Cell|None:
    if len(Cell.grid) == 0:
        return None
    for cell in Cell.grid:
        if cell.get_pos() == ig_pos:
            return cell
    return None

def purge_cells()->None:
    for cell in Cell.grid:
        if not cell.get_state():
            need_purge = True
            ig_pos = cell.get_pos()
            for x in range(ig_pos[0]-1,ig_pos[0]+2):
                    for y in range(ig_pos[1]-1,ig_pos[1]+2):
                        result = check_grid((x,y))
                        if result is not None:
                            if result.get_state():
                                need_purge = False
            if need_purge:
                Cell.grid.remove(cell)
    return

def calcul_next_grid()->None:
    for cell in Cell.grid:
        neighbours = 0
        ig_pos = cell.get_pos()
        for x in range(ig_pos[0]-1,ig_pos[0]+2):
                for y in range(ig_pos[1]-1,ig_pos[1]+2):
                    result = check_grid((x,y))
                    if result is not None and (x,y) != ig_pos:
                        if result.get_state():
                            neighbours += 1
        if cell.get_state():
            if 2 <= neighbours <= 3:
                cell.set_next_state(True)
            else:
                cell.set_next_state(False)
        else:
            if neighbours == 3:
                cell.set_next_state(True)
            else:
                cell.set_next_state(False)
    return

def update_grid()->None:
    for cell in Cell.grid:
        cell.set_state(cell.get_next_state())
    return
pygame.init()
pygame.display.set_caption('Game of life')
screen = pygame.display.set_mode((1200, 700), pygame.RESIZABLE)
font = pygame.font.SysFont("Arial",24)
size = 100
timee = time.time()
timing = 1
state = "start"

while state != "stop":

    for event in pygame.event.get():
        if event.type == QUIT:
            state = "stop"
        if state == "start":
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                found = check_grid(convert_mouse_pos(mouse_pos))
                if found == None:
                    place_cell(mouse_pos)
                else:
                    found.change_state()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = "play"  
        #choose a speed at any time
    
    if state == "play":
        if len(Cell.grid) != 0:#+if not stay still fo multiple turns
            #print(time.time())
            #find a way to limit op/s
            if time.time() - timee >= timing:
                timee = time.time()
                print("calcul...")
                calcul_next_grid()
                print("update...")
                update_grid()
                print("purge...")
                purge_cells()
                print("end...")
    # render ----------------------------------------------------------------{)
    screen.fill((59,59,63))
    for cell in Cell.grid:
        if cell.get_state():
            pygame.draw.rect(screen,(255,255,255),draw_cell(cell))
        
    pygame.display.update()
    #print(len(Cell.grid))

pygame.quit()
sys.exit()





    
    
    