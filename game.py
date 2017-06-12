#GEM CRUSH
import pygame, sys, random, math
from pygame.locals import *

backgroundImageDirectory = "images/background.jpg"
borderImageDirectory = "images/border.png"
imageBomb = "images/bomb.png"
imageDiamondMandarina = "images/portokal.png"
imageDiamondSinko = "images/sinko.png"
imageDiamondMore = "images/more.png"
imageDiamondEmerald = "images/emerald.png"
imageDiamondRubin = "images/rubin.png"
imageDiamondIce = "images/ice.png"
imageDiamondDrugoSinko = "images/drugosinko.png"
imageDiamondLilavo = "images/lilavo.png"

pygame.init()
screen = pygame.display.set_mode((700, 700), 0, 32)
background = pygame.image.load(backgroundImageDirectory).convert()
border = pygame.image.load(borderImageDirectory).convert_alpha()

gems = {
    "Mandarina": pygame.image.load(imageDiamondMandarina).convert_alpha(),
    "Sinko": pygame.image.load(imageDiamondSinko).convert_alpha(),
    "More": pygame.image.load(imageDiamondMore).convert_alpha(),
    "Emerald": pygame.image.load(imageDiamondEmerald).convert_alpha(),
    "Ruby": pygame.image.load(imageDiamondRubin).convert_alpha(),
    "Ice": pygame.image.load(imageDiamondIce).convert_alpha(),
    "DrugoSinko": pygame.image.load(imageDiamondDrugoSinko).convert_alpha(),
    "Purple": pygame.image.load(imageDiamondLilavo).convert_alpha()
}

selectedDiamond = None
grid = [[]]
imagesize = 24
difference = 2
linesize = 0
size = imagesize + linesize


class Diamond:
    def __init__(self):
        key = random.sample(gems.keys(), 1)[0]
        self.image = gems[key]
        self.type = key
        self.selected = False


def CheckForDestruction(gem):
    horizontal = [gem]
    vertical = [gem]
    right = GetDiamondFromCoords(gem.x, gem.y+imagesize)
    left = GetDiamondFromCoords(gem.x, gem.y-imagesize)
    if right and right.type == gem.type:
        horizontal.append(right)
        right2 = GetDiamondFromCoords(gem.x, gem.y+imagesize)
        if right2 and right2.type == gem.type:
            horizontal.append(right2)

    if left and left.type == gem.type:
        horizontal.append(left)
        left2 = GetDiamondFromCoords(gem.x, gem.y-imagesize)
        if left2 and left2.type == gem.type:
            horizontal.append(left2)

    for diamond in horizontal:
        diamond.selected = True
    print('-------------')
    if len(horizontal) > 2:
        print("DAAAAAAAAAAAAAAAA")
        print(gem.type)
    if len(vertical) > 2:
        pass


def GetDiamondFromCoords(x, y):
    for row in grid:
        for diamond in row:
            if x >= diamond.x and x <= diamond.x + imagesize and y >= diamond.y and y <= diamond.y + imagesize:
                return diamond
    return None

def GetDiamondFromMouseCoords():
    x, y = pygame.mouse.get_pos()
    for row in grid:
        for diamond in row:
            if x >= diamond.x and x <= diamond.x + imagesize and y >= diamond.y and y <= diamond.y + imagesize:
                return diamond
    return None


def SpawnDiamonds():
    i, j = 0, 0
    for x in range(9, 20):

        grid.append([])
        j = 0
        for y in range(9, 20):
            currentDiamond = Diamond(x, y)
            if (i == 0 or i == 10) and not (j == 0 or j == 1):
                while currentDiamond.type == grid[i][j - 2].type and currentDiamond.type == grid[i][j - 1].type:
                    currentDiamond = Diamond(x, y)
            if (j == 0 or j == 10) and not (i == 0 or i == 1):
                while currentDiamond.type == grid[i - 1][j].type and currentDiamond.type == grid[i - 2][j].type:
                    currentDiamond = Diamond(x, y)
            if i >= 2 and j >= 2:
                while (currentDiamond.type == grid[i][j - 1].type and currentDiamond.type == grid[i][j - 2].type) or (
                        currentDiamond.type == grid[i - 1][j].type and currentDiamond.type == grid[i - 2][j].type):
                    currentDiamond = Diamond(x, y)
            grid[i].append(currentDiamond)
            j += 1
        i += 1


def NotDiagonal():
    a = abs(selectedDiamond.x - secondDiamond.x) == size
    b = abs(selectedDiamond.y - secondDiamond.y) == size
    if a and b:
        return False
    else:
        return a or b


SpawnDiamonds()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if selectedDiamond == None:
                selectedDiamond = GetDiamondFromMouseCoords()
                if selectedDiamond:
                    selectedDiamond.selected = True
            else:
                secondDiamond = GetDiamondFromMouseCoords()
                if secondDiamond:
                    if selectedDiamond != None and selectedDiamond != secondDiamond and NotDiagonal():
                        '''IZNESI VUV FUNKCIQ'''
                        temp = secondDiamond.x
                        secondDiamond.x = selectedDiamond.x
                        selectedDiamond.x = temp
                        temp = secondDiamond.y
                        secondDiamond.y = selectedDiamond.y
                        selectedDiamond.y = temp
                        CheckForDestruction(selectedDiamond)
                        print(selectedDiamond.type)
                selectedDiamond.selected = False
                selectedDiamond = None
        if event.type == MOUSEBUTTONUP:
            pass

    screen.blit(background, (0, 0))

    for i in range(0, 11):
        for j in range(0, 11):
            diamond = grid[i][j]
            if diamond.selected:

                newimage = pygame.transform.scale(diamond.image,
                                                  (imagesize - (difference * 2), imagesize - (difference * 2)))
                screen.blit(newimage, (diamond.x + difference, diamond.y + difference))
                screen.blit(border, (diamond.x, diamond.y))
            else:
                screen.blit(diamond.image, (diamond.x, diamond.y))

    pygame.display.update()
