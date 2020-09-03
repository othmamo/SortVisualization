import pygame
import random
import time
from pygame.locals import *

pygame.init()
#width and height of screen
width=800
height=600
window = pygame.display.set_mode((width+200,height+200))
screen = pygame.Surface((width,height))
img_list = pygame.image.load(r'Size.png')
add=[None,None]

bars=[]
buttons=[]
butFont = pygame.font.SysFont('comicsans',25)
loop=0
bars=[]
numbers=[]
speed=0.3
size_list=1

class Button():
    def __init__(self,text, sizeX, sizeY, posX, posY, color=(156,158,159)):
        self.text=text
        self.posX=posX
        self.posY=posY
        self.sizeX=sizeX
        self.color=color
        self.sizeY=sizeY
        self.launch=False
        self.rect=None
        self.enable=False

    def drawText(self):
        self.rect=pygame.draw.rect(window, self.color, (self.posX, self.posY, self.sizeX, self.sizeY), 0)
        img = butFont.render(self.text, True, (255,255,255))
        sizeOfImg=butFont.size(str(self.text))
        window.blit(img, (self.posX+(self.sizeX-sizeOfImg[0])//2, self.posY+(self.sizeY-sizeOfImg[1])//2))

    def collide(self,pos):
        if(self.rect):
            return self.rect.collidepoint(pos)

class Bar(pygame.sprite.Sprite):
    def __init__(self, number, sizeX, sizeY, posX, posY, color=(0,200,255)):
        super(Bar, self).__init__()
        self.position = (posX, posY)
        self.size=(sizeX,sizeY)
        self.number=number
        self.surf = pygame.Surface(self.size)
        self.rect = self.surf.get_rect()
        self.surf.fill(color)
        self.font=None
        if(len(bars)<=50):
            self.font = pygame.font.SysFont('comicsans', min(int(self.size[0]*0.75),int(self.size[1])))
        self.printNumber()

    def changeColor(self,color):
        self.surf.fill(color)
        self.printNumber()

    def printNumber(self):
        if(len(bars)>50):
            return
        img = self.font.render(str(self.number), True, (255,255,255))
        sizeOfImg=self.font.size(str(self.number))
        self.surf.blit(img,((self.size[0]-sizeOfImg[0])//2,self.size[1]-sizeOfImg[1]))

def buildMap(L, i, j):
    """Function that return a list of bars with good size and positions
    depending of the elements to sort on listL"""
    isZero = 1 if min(L)==0 else 0
    ladderH=height//(max(L)+isZero)
    ladderW=width//len(L)
    for k in range(i,j+1):
        bars[k]=(Bar(L[k], ladderW, ladderH*(L[k]+isZero),k*ladderW, height-ladderH*(L[k]+isZero)))

def draw(L, i, j):
    if(i!=j):
        blackSurf = pygame.Surface((L[i].size[0]+L[j].size[0],max(L[i].size[1],L[j].size[1])))
        screen.blit(blackSurf,(min(L[i].position[0],L[j].position[0]), height-max(L[i].size[1],L[j].size[1])))
    for k in range(i,j+1):
        #borders
        if len(L)<=width//4 :
            pygame.draw.rect(L[k].surf,(0,0,0),L[k].rect,1)
        screen.blit(L[k].surf,L[k].position)
        window.blit(screen, ((200)//2,200))
    pygame.display.flip()

def draw_swap(L,i,j):
    blackSurf = pygame.Surface((L[i].size[0],max(L[i].size[1],L[j].size[1])))
    screen.blit(blackSurf,(L[i].position[0], height-max(L[i].size[1],L[j].size[1])))
    screen.blit(blackSurf,(L[j].position[0], height-max(L[i].size[1],L[j].size[1])))
    if len(L)<=width//4 :
        pygame.draw.rect(L[i].surf,(0,0,0),L[i].rect,1)
        pygame.draw.rect(L[j].surf,(0,0,0),L[j].rect,1)
    screen.blit(L[i].surf,L[i].position)
    screen.blit(L[j].surf,L[j].position)
    window.blit(screen, ((200)//2,200))
    pygame.display.flip()

def randomList(i):
    L=[]
    for i in range(i):
        L.append(random.randint(0,30))
    return L

def recolorAll(color, i, j):
    for k in range(i,j+1):
        bars[k].changeColor(color)

def normal_swap(arr,i,j):
    arr[i], arr[j] = arr[j], arr[i]
    buildMap(arr,i,i)
    buildMap(arr,j,j)
    draw_swap(bars,i,j)

def swap_design(arr,i,j):
    bars[j].changeColor((255,0,0))
    bars[i].changeColor((255,0,0))
    draw(bars,j,j)
    draw(bars,i,i)
    time.sleep(speed)
    arr[i], arr[j] = arr[j], arr[i]
    buildMap(arr,i,i)
    buildMap(arr,j,j)
    draw_swap(bars,i,j)
    bars[j].changeColor((0,255,0))
    bars[i].changeColor((0,255,0))
    draw(bars,j,j)
    draw(bars,i,i)
    time.sleep(speed)
    recolorAll((0,200,255), j, j)
    recolorAll((0,200,255), i, i)
    draw(bars,j,j)
    draw(bars,i,i)

def sort_aux (L,node,n):
    k = node
    j = 2*k
    while (j<=n):
        if(not close()):
            return 0
        if (j<n and L[j]<L[j+1]):
            j+=1
        if (L[k]<L[j]):
            if(size_list<=175):
                swap_design(L,j,k)
            else:
                normal_swap(L,j,k)
            k=j
            j=2*k
        else:
            break

def heap_sort(L):
    l=len(L)
    i=l//2
    j=l-1
    while (i>=0):
        if(sort_aux(L,i,l-1)==0):
            return 0
        i-=1
    while(j>=1):
        if(size_list<=175):
            swap_design(L,0,j)
        else:
            normal_swap(L,0,j)
        if (sort_aux(L,0,j-1)==0):
            return 0
        j-=1
    return 1

def partition(arr, l, h, bars):
    i = ( l - 1 )
    x = arr[h]
    if(len(arr)<=150):
        bars[h].changeColor((240,240,120))
        draw(bars, h,h)
    for j in range(l, h):
        if(not close()):
            return -1
        if   arr[j] <= x:
            if(i!=j):
                i = i + 1
                if(size_list<=150):
                    swap_design(arr,i,j)
                else:
                    normal_swap(arr,i,j)
    if(i+1!=h):
        if(size_list<=150):
            swap_design(arr,i+1,h)
        else:
            normal_swap(arr,i+1,h)
    recolorAll((0,200,255), h, h)
    draw(bars,h,h)
    return (i + 1)

def quickSortIterative(arr, l, h, bars):
    size = h - l + 1
    stack = [0] * (size)
    top = -1
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h
    while top >= 0:

        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1

        p = partition( arr, l, h, bars)
        if(p==-1):
            return 0

        if p-1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1

        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h
    return 1


#Return 0 if close the window and 1 if end of sort
def bubbleSort(L,bars):
    for i in range(len(L)-1):
        end=True
        for j in range(len(L)-i-1):
            if(not close()):
                return 0
            if L[j] > L[j+1] :
                end=False
                if(len(bars)<=150):
                    bars[j].changeColor((255,0,0))
                    bars[j+1].changeColor((255,0,0))
                    draw(bars, j, j+1)
                    time.sleep(speed)
                L[j], L[j+1] = L[j+1], L[j]
                buildMap(L,j,j+1)
                draw(bars, j, j+1)
            if(len(bars)<=150):
                bars[j].changeColor((0,255,0))
                bars[j+1].changeColor((0,255,0))
                draw(bars, j, j+1)
                time.sleep(speed)
            recolorAll((0,200,255), j, j+1)
            draw(bars,j,j+1)
        if(end==True):
            return 1
        draw(bars,0,len(L)-1)
    return -1

def close():
    for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    return False
            elif event.type == QUIT:
                return False
    return True

def create_random():
    global speed, numbers, bars, loop
    bars.clear
    numbers.clear
    screen.fill((0,0,0))
    loop=0
    numbers=randomList(size_list)
    bars=[None]*len(numbers)
    buildMap(numbers, 0, len(numbers)-1)
    draw(bars, 0, len(bars)-1)

def initButtons():
    global size_list
    global add, remove
    widthBut=int((width+200)/5*0.7)
    posXBut=int((width+200)/5*0.15)
    for i in range(5):
        buttons.append(Button("", widthBut, widthBut//2, posXBut+i*((width+200)//5), 50))
    buttons[0].text="Create List"
    buttons[0].enable=True
    buttons[1].text="Bubble Sort"
    buttons[2].text="Quick Sort"
    buttons[3].text="Heap Sort"
    buttons[4].text="Start !"
    for i in range(5):
        buttons[i].drawText()

    #Button to add size of list
    add[0]=Button("", 31,32,posXBut+2*((width+200)//5)+109, 50+widthBut//2+10)
    add[0].drawText()
    add[1]=Button("", 31,33,posXBut+2*((width+200)//5)+109, 50+widthBut//2+10+34)
    add[1].drawText()

    print_size(size_list)

def print_size(i):
    widthBut=int((width+200)/5*0.7)
    posXBut=int((width+200)/5*0.15)
    window.blit(img_list, (posXBut+2*((width+200)//5), 50+widthBut//2+10))
    img = butFont.render(str(i), True, (0,0,0))
    sizeOfImg=butFont.size(str(i))
    window.blit(img, ((posXBut+2*((width+200)//5)+9+(91-sizeOfImg[0])//2, 50+widthBut//2+10+9+(49-sizeOfImg[1])//2)))


def disenable_launch(L, b):
    for i in range(1,len(L)-1):
        L[i].enable=b

def unenlaunch_launch(L, b):
    for i in range(1,len(L)-1):
        L[i].launch=b

def whatToDo():
    global size_list
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if(add[0].collide(pos) and buttons[0].enable==True):
            size_list=min(size_list+1,800)
            print_size(size_list)
        if(add[1].collide(pos) and buttons[0].enable==True):
            size_list-=1
            if(size_list<1):
                size_list=1
            print_size(size_list)
        for i in range(len(buttons)):
            if(buttons[i].collide(pos) and buttons[i].enable):
                if(1<=i<=3):
                    unenlaunch_launch(buttons, False)
                buttons[i].launch=True

def restart():
    unenlaunch_launch(buttons, False)
    disenable_launch(buttons, False)
    add[0].enable=True
    add[1].enable=True
    buttons[0].launch=False
    buttons[-1].launch=False
    buttons[-1].enable=False
    buttons[0].enable=True

initButtons()
while(close()):
    if(buttons[0].launch==True):
        create_random()
        add[0].enable=False
        add[1].enable=False
        buttons[0].launch=False
        buttons[0].enable=False
        disenable_launch(buttons, True)
        buttons[-1].enable=True
    if(buttons[-1].launch==True):
        if(buttons[1].launch==True):
            speed/=(len(bars)/10)
            if(len(bars)>=60):
                speed=0
            value=bubbleSort(numbers, bars)
            if(value==1):
                restart()
                continue
            elif(value==0):
                break
        elif(buttons[2].launch==True):
            speed=0.3/(len(bars)/10)
            if(len(bars)>150):
                speed=0
            value=quickSortIterative(numbers,0,len(bars)-1, bars)
            if(value==1):
                restart()
                continue
            elif(value==0):
                break
        elif(buttons[3].launch==True):
            speed=0.3/(len(bars)/10)
            if(len(bars)>150):
                speed=0
            value=heap_sort(numbers)
            if(value==1):
                restart()
                continue
            elif(value==0):
                break
    whatToDo()
    pygame.display.flip()


pygame.quit()
