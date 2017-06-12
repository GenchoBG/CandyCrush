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

grid = [[]]
selectedDiamond = None
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


def SpawnDiamonds():
    i, j = 0, 0
    for x in range(0, 11):
        grid.append([])
        j = 0
        for y in range(0, 11):
            currentDiamond = Diamond()
            try:
                while grid[i][j - 1].type == currentDiamond.type and grid[i][j - 2].type == currentDiamond.type:
                    currentDiamond = Diamond()
            except(IndexError):
                pass
            try:
                while grid[i - 1][j].type == currentDiamond.type and grid[i - 2][j].type == currentDiamond.type:
                    currentDiamond = Diamond()
            except(IndexError):
                pass
            grid[i].append(currentDiamond)
            j += 1
        i += 1


def ForeachDiamondsX(coord1, coord2, diamondY, list, diamond):
    for x in range(coord1, coord2):
        if grid[x][diamondY].type == diamond.type:
            list.append(diamond)
        else:
            break


def ForeachDiamondsY(coord1, coord2, diamondX, list, diamond):
    for y in range(coord1, coord2):
        if grid[diamondX][y].type == diamond.type:
            list.append(diamond)
        else:
            break


def CheckForDestruction(diamond):
    destruction = False
    diamondX, diamondY = GetCoordsFromArray(diamond)
    horizontalDiamonds = [diamond]
    verticalDiamonds = [diamond]

    ForeachDiamondsX(diamondX + 1, 11, diamondY, horizontalDiamonds, diamond)
    ForeachDiamondsX(0, diamondX, diamondY, horizontalDiamonds, diamond)

    ForeachDiamondsY(diamondY+1, 11, diamondX, verticalDiamonds, diamond)
    ForeachDiamondsY(0, diamondY, diamondX, verticalDiamonds, diamond)

    if len(horizontalDiamonds) >= 3:
        print("didko e pedal")
    if len(verticalDiamonds) >= 3:
        print("vertikalno")

    return destruction


def GetDiamondFromMouseCoords():
    i, j = pygame.mouse.get_pos()
    i = math.floor(i / 25)
    j = math.floor(j / 25)
    try:
        return grid[i][j]
    except IndexError:
        return None


def GetCoordsFromArray(diamond):
    for i in range(0, 11):
        for j in range(0, 11):
            if grid[i][j] == diamond:
                return i, j


def Adjacent(firstDiamond, secondDiamond):
    x1, y1 = GetCoordsFromArray(firstDiamond)
    x2, y2 = GetCoordsFromArray(secondDiamond)
    xDifference = abs(x1 - x2)
    yDifference = abs(y1 - y2)
    return (xDifference == 1 and yDifference == 0) or (xDifference == 0 and yDifference == 1)


def Swap(firstDiamond, secondDiamond):
    if Adjacent(firstDiamond, secondDiamond):
        temp = firstDiamond.type
        firstDiamond.type = secondDiamond.type
        secondDiamond.type = temp
        temp = firstDiamond.image
        firstDiamond.image = secondDiamond.image
        secondDiamond.image = temp


SpawnDiamonds()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if selectedDiamond == None:
                selectedDiamond = GetDiamondFromMouseCoords()
                selectedDiamond.selected = True
            else:
                secondDiamond = GetDiamondFromMouseCoords()
                if secondDiamond:
                    Swap(selectedDiamond, secondDiamond)
                    CheckForDestruction(selectedDiamond)
                    CheckForDestruction(secondDiamond)
                    selectedDiamond.selected = False
                    selectedDiamond = None
                    secondDiamond = None

    screen.blit(background, (0, 0))

    for i in range(0, 11):
        for j in range(0, 11):
            diamond = grid[i][j]
            if diamond.selected:

                newimage = pygame.transform.scale(diamond.image,
                                                  (imagesize - (difference * 2), imagesize - (difference * 2)))
                screen.blit(newimage, (i * 25 + difference, j * 25 + difference))
                screen.blit(border, (i * 25 + difference, j * 25 + difference))
            else:
                screen.blit(diamond.image, (i * 25 + difference, j * 25 + difference))

    pygame.display.update()
