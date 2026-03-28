# /ᐠ｡ꞈ｡ᐟ\
#PRIO! séparer les fichier !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#TODO: add visible grid (fait la grid plus tard Harry), mouvement[V], zoom[V], save, load, (option : retour menu, speed), win_size mini 

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
    def draw_cell(self,screen:pygame.Surface)->None:
        cell_pos = convert_ig_pos(self.__ig_pos)
        pygame.draw.rect(screen,(255,255,255),(cell_pos[0],cell_pos[1],size,size))
        return  
class Button():
    def __init__(self,pos:tuple[int,int],width:int,height:int)->None:
        self.__pos = (win_size[0]-pos[0],win_size[1]-pos[1])
        self.__width = width
        self.__height = height
        self.default_param = (win_size,pos)
        return   
    def update_pos(self)->None:
        self.__pos = (win_size[0]-self.default_param[1][0],win_size[1]-self.default_param[1][1])
        return 
    def get_size(self)->tuple[int,int]:
        return self.__width,self.__height
    def get_pos(self)->tuple[int,int]:
        return self.__pos
    def draw_button(self,screen:pygame.Surface)->None:
        pygame.draw.rect(screen,(255,255,255),(self.__pos[0],self.__pos[1],self.__width,self.__height))
        return
class Contexte_window():
    def __init__(self,title:str,content:str,size:tuple[int,int])->None:
        self.__title = title
        self.__content = content
        self.__size = size
        return

def place_cell(mouse_pos:tuple[int,int])->None:
    Cell(convert_mouse_pos(mouse_pos),True)
    return
def convert_mouse_pos(mouse_pos:tuple[int,int])->tuple[int,int]:
    win_size = pygame.display.get_window_size()
    return (mouse_pos[0]+x_offset-win_size[0]//2)//size,(mouse_pos[1]+y_offset-win_size[1]//2)//size
def convert_ig_pos(ig_pos:tuple[int,int])->tuple[int,int]:
    win_size = pygame.display.get_window_size()
    return ig_pos[0]*size-x_offset+win_size[0]//2,ig_pos[1]*size-y_offset+win_size[1]//2
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
def save(name:str)->None: #-------------------------------------------------------------------------------------------------------
    purge_cells()
    """try:
        file = open("saves/"+name,'x')
    except FileExistsError:
        rewrite_win = Contexte_window()
    #    file = open("saves/"+name,'w')
    
    #file.close()"""
    return

pygame.init()
pygame.display.set_caption('Game of life')
screen = pygame.display.set_mode((1200, 700), pygame.RESIZABLE)
font = pygame.font.SysFont("Arial",24)
size = 100
timee = time.time()
timing = 1
up, down, left, right, zoom, unzoom = False, False, False, False, False, False
x_offset, y_offset = 0,0
win_size = pygame.display.get_window_size()
save_button = Button((220,120),200,100)
save("yo")
state = "start"

while state != "stop":

    for event in pygame.event.get():
        if event.type == QUIT:
            state = "stop"
        if event.type == MOUSEBUTTONDOWN and state == "start":
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                save_b_pos = save_button.get_pos()
                if   save_b_pos[0] <= mouse_pos[0] <= save_b_pos[0] + save_button.get_size()[0] and save_b_pos[1] <= mouse_pos[1] <= save_b_pos[1] + save_button.get_size()[1]:
                    save_win = Contexte_window("Save","What is the name of your savefile",(1000,1000))
                    #---------------------------------------------------------------------------
                    save(input())
                else:
                    found = check_grid(convert_mouse_pos(mouse_pos))
                    if found == None:
                        place_cell(mouse_pos)
                    else:
                        found.change_state()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE and state == "start":
                state = "play"  
            if event.key == K_z or event.key == K_w:
                up = True
            elif event.key == K_s:
                down = True
            if event.key == K_q or event.key == K_a:
                left = True
            elif event.key == K_d:
                right = True
            if event.key == K_UP:
                zoom = True
            elif event.key == K_DOWN:
                unzoom = True
        elif event.type == KEYUP:
                if event.key == K_z or event.key == K_w:
                    up = False
                elif event.key == K_s:
                    down = False
                if event.key == K_q or event.key == K_a:
                    left = False
                elif event.key == K_d:
                    right = False
                if event.key == K_UP:
                    zoom = False
                elif event.key == K_DOWN:
                    unzoom = False
        #choose a speed at any time
    if up:
        y_offset -= 1
    elif down:
        y_offset += 1
    if left:
        x_offset -= 1
    elif right:
        x_offset += 1
    if zoom:
        if size < 100:
            size += 1
    elif unzoom:
        if size > 1:
            size -= 1

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
            cell.draw_cell(screen)
    if state == "start":
        win_size = pygame.display.get_window_size()
        save_button.update_pos()
        save_button.draw_button(screen)
    pygame.display.update()
    #print(len(Cell.grid))

pygame.quit()
sys.exit()
