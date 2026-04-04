# /ᐠ｡ꞈ｡ᐟ\
#TODO: add visible grid (fait la grid plus tard Harry), pas modif les Cells quand click on win, save, load, (option : retour menu, speed), win_size mini 
# reminder: prio 0->5 : cells->rewrite_sure_button
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
    def __str__(self) -> str:
        return str(self.__ig_pos)
class Button():
    def __init__(self,title:str,priority:int,pos:tuple[int,int],width:int,height:int)->None:
        self.__title = title
        self.__priority = priority
        self.__pos = pos
        self.__width = width
        self.__height = height
        self.__reduction_ratio = (win_size[0]/pos[0],win_size[1]/pos[1])
        return   
    def get_size(self)->tuple[int,int]:
        return self.__width,self.__height
    def get_pos(self)->tuple[int,int]:
        return self.__pos
    def get_prio(self)->int:
        return self.__priority
    def is_collided(self,pos:tuple[int,int])->bool:
        if self.__pos[0]-self.__width//2 <= pos[0] <= self.__pos[0]+self.__width//2 and self.__pos[1]-self.__height//2 <= pos[1] <= self.__pos[1]+self.__height//2:
            return True
        return False
    def draw_button(self)->None:
        self.__pos = (win_size[0]//self.__reduction_ratio[0],win_size[1]//self.__reduction_ratio[1])
        pygame.draw.rect(screen,(42,14,143),(self.__pos[0]-self.__width//2,self.__pos[1]-self.__height//2,self.__width,self.__height))
        return
    def __str__(self) -> str:
        return self.__title
class Contexte_window():
    def __init__(self,title:str,priority:int,size:int)->None:
        self.__title = title
        self.__priority = priority
        self.__size = size
        return
    def get_prio(self)->int:
        return self.__priority
    def display(self)->None:
        match self.__size:
            case 0: # SMALL
                h = 0 #temp
                v = 0 #temp
            case 2: # BIG
                h = win_size[0]/8
                v = win_size[1]/16
            case _:
                print("error: size not understood")
                return
        pygame.draw.rect(screen,(255,255,255),(h,v,win_size[0]-2*h,win_size[1]-2*v))
        match self.__title:
            case "Save":
                pos = ((win_size[0]/2)-(15*len(self.__title)/2),win_size[1]/8)
                text = font.render(self.__title,True,(0,0,0))
                screen.blit(text,pos)
                pos = ((win_size[0]/2)-190,(win_size[1]/8)+20)
                text = font.render("What is the name of your savefile?",True,(0,0,0))
                screen.blit(text,pos)
        #temp
        pygame.draw.rect(screen,(0,0,0),((win_size[0]/2)-1,0,2,win_size[1])) # middle line
        return
    def __str__(self) -> str:
        return self.__title

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
    try:
        file = open("saves/"+name,'x')
    except FileExistsError:
        rewrite_win = Contexte_window("Rewrite",4,SMALL)
        return # temp
        file = open("saves/"+name,'w') # rewrite anyway for now
    for c in Cell.grid:
        if c.get_state():
            file.write(c.__str__())
    file.close()
    return

pygame.init()
pygame.display.set_caption('Game of life')
screen = pygame.display.set_mode((1200, 700), pygame.RESIZABLE)
win_size = pygame.display.get_window_size()
font = pygame.font.SysFont("Arial",24)
timee = time.time()
size = 100
timing = 1
x_offset, y_offset = 0,0
up, down, left, right, zoom, unzoom = False, False, False, False, False, False

# enum win.size (+/-)
SMALL = 0
MEDIUM = 1
BIG = 2

save_button, save_done_button, save_return_button = None, None, None
save_win, rewrite_win = None,None
state = "start"

while state != "stop":

    for event in pygame.event.get():
        if event.type == QUIT:
            state = "stop"
        if event.type == MOUSEBUTTONDOWN and state == "start":
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if save_done_button is not None and save_done_button.is_collided(mouse_pos):
                   save("autosave")  
                #elif save_return_button:
                elif save_button is not None and save_button.is_collided(mouse_pos):
                    if save_win is None:
                        save_win = Contexte_window("Save",2,BIG)
                
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
    
    win_size = pygame.display.get_window_size()
    buttons = [save_button, save_done_button, save_return_button]
    wins = [save_win, rewrite_win]

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

    if state == "start":
        if save_button is None:
            save_button = Button("Save",1,(win_size[0]-110,win_size[1]-60),200,100)
    elif state == "play":
        if len(Cell.grid) != 0:#+if not stay still fo multiple turns
            #print(time.time())
            #find a way to limit op/s
            if time.time() - timee >= timing:
                timee = time.time()
                calcul_next_grid()
                update_grid()
                purge_cells()
    if save_win is not None:
        if save_done_button is None:
            save_done_button = Button("Done",3,(win_size[0]//3,win_size[1]-win_size[1]//4),200,100)
        if save_return_button is None:
            save_return_button = Button("Return",3,(win_size[0]-win_size[0]//3,win_size[1]-win_size[1]//4),200,100)

    # render ----------------------------------------------------------------{)
    screen.fill((59,59,63))
    for cell in Cell.grid: # prio 0
        if cell.get_state():
            cell.draw_cell(screen)
            
    if state == "start":
        for prio in range(1,6):
            for b in buttons:
                if b is not None and b.get_prio() == prio:
                    b.draw_button()
            for w in wins:
                if w is not None and w.get_prio() == prio:
                    w.display()

    pygame.display.update()
    #print(len(Cell.grid))

pygame.quit()
sys.exit()
