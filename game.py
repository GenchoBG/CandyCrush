import pygame, sys, random, math
from pygame.locals import *

backgroundImageDirectory = "images/background.jpg"
imageDiamondMandarina = "images/portokal.png"
imageDiamondSinko = "images/sinko.png"
imageDiamondMore = "images/more.png"
imageDiamondEmerald = "images/emerald.png"
imageDiamondRubin = "images/rubin.png"

pygame.init()
screen = pygame.display.set_mode((700, 700), 0, 32)
background = pygame.image.load(backgroundImageDirectory).convert()
diamondMandarina = pygame.image.load(imageDiamondMandarina).convert_alpha()
diamondSinko = pygame.image.load(imageDiamondSinko).convert_alpha()

images = [diamondMandarina, diamondSinko]

images.append(pygame.image.load(imageDiamondMore).convert_alpha())
images.append(pygame.image.load(imageDiamondEmerald).convert_alpha())
images.append(pygame.image.load(imageDiamondRubin).convert_alpha())

selectedDiamond = None
grid = []
imagesize = 25
linesize = 0
size = imagesize + linesize


class Diamond:
    def __init__(self, x, y):
        self.x = x * imagesize  # za da ne se zalepvat 1 vurhu drug t.e. setvane na pravilni koordinati
        self.y = y * imagesize
        self.image = images[random.randint(0, len(images) - 1)]
        self.selected = False


def GetDiamondFromMouseCoords():
    x, y = pygame.mouse.get_pos()
    for diamond in grid:
        if x >= diamond.x and x <= diamond.x + imagesize and y >= diamond.y and y <= diamond.y + imagesize:
            return diamond
    return None


for x in range(9, 20):
    for y in range(9, 20):
        grid.append(Diamond(x, y))


def Something():
    a = abs(selectedDiamond.x - secondDiamond.x) == size
    b = abs(selectedDiamond.y - secondDiamond.y) == size
    if a and b:
        return False
    else:
        return a or b


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if selectedDiamond == None:
                selectedDiamond = GetDiamondFromMouseCoords()
            else:
                secondDiamond = GetDiamondFromMouseCoords()
                if selectedDiamond != None and selectedDiamond != secondDiamond and Something():
                    '''IZNESI VUV FUNKCIQ'''
                    temp = secondDiamond.x
                    secondDiamond.x = selectedDiamond.x
                    selectedDiamond.x = temp
                    temp = secondDiamond.y
                    secondDiamond.y = selectedDiamond.y
                    selectedDiamond.y = temp
                selectedDiamond = None
        if event.type == MOUSEBUTTONUP:
            pass

    screen.blit(background, (0, 0))

    for diamond in grid:
        screen.blit(diamond.image, (diamond.x, diamond.y))

    pygame.display.update()
