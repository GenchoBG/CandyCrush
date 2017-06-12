import pygame, sys, random, math
from pygame.locals import *

clock = pygame.time.Clock()
minutes = 0
seconds = 0
milliseconds = 0

backgroundImageDirectory = "images/background.png"
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

score = 0
grid = [[]]
selectedDiamond = None
imagesize = 24
difference = 2
linesize = 0
size = imagesize + linesize

myfont = pygame.font.SysFont("monospace", 18)

highscore = 0
with open("highscore.txt", "r") as f:
    highscore = int(f.read())

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



def Destroy(diamonds):
    if diamonds and len(diamonds) >= 2:
        for diamond in diamonds:
            if diamond:
                row, col = GetCoordsFromArray(diamond)
                grid[row][col] = None



def CheckForDestruction(diamond):
    diamondX, diamondY = GetCoordsFromArray(diamond)
    horizontalDiamonds = []
    verticalDiamonds = []

    '''nadqsno'''
    index = diamondX + 1
    while index < 11 and grid[index][diamondY].type == diamond.type:
        horizontalDiamonds.append(grid[index][diamondY])
        index += 1

    '''nalqvo'''
    index = diamondX - 1
    while index >= 0 and grid[index][diamondY].type == diamond.type:
        horizontalDiamonds.append(grid[index][diamondY])
        index -= 1

    '''nadolu'''
    index = diamondY + 1
    while index < 11 and grid[diamondX][index].type == diamond.type:
        verticalDiamonds.append(grid[diamondX][index])
        index += 1

    '''nagore'''
    index = diamondY - 1
    while index >= 0 and grid[diamondX][index].type == diamond.type:
        verticalDiamonds.append(grid[diamondX][index])
        index -= 1

    toDestroy = []

    if len(horizontalDiamonds) >= 2:
        print(str(len(horizontalDiamonds) + 1) + " horizontalno " + str(horizontalDiamonds[0].type))
        for d in horizontalDiamonds:
            toDestroy.append(d)
    if len(verticalDiamonds) >= 2:
        for d in verticalDiamonds:
            toDestroy.append(d)
        print(str(len(verticalDiamonds) + 1) + " vertikalno " + str(verticalDiamonds[0].type))
    if len(verticalDiamonds) >= 2 or len(horizontalDiamonds) >= 2:
        toDestroy.append(diamond)

    for d in toDestroy:
        d.selected = True

    Destroy(toDestroy)


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
try:
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
                        selectedDiamond.selected = False
                        Swap(selectedDiamond, secondDiamond)
                        CheckForDestruction(selectedDiamond)
                        CheckForDestruction(secondDiamond)
                        score += 1
                    selectedDiamond = None
                    secondDiamond = None

        screen.blit(background, (0, 0))

        for i in range(0, 11):
            for j in range(0, 11):
                diamond = grid[i][j]
                if diamond:
                    if diamond.selected:

                        newimage = pygame.transform.scale(diamond.image,
                                                          (imagesize - (difference * 2), imagesize - (difference * 2)))
                        screen.blit(newimage, (i * 25 + difference, j * 25 + difference))
                        screen.blit(border, (i * 25 + difference, j * 25 + difference))
                    else:
                        screen.blit(diamond.image, (i * 25 + difference, j * 25 + difference))

        scorelabel = myfont.render("Score: " + str(score), 1, (255, 255, 0))
        screen.blit(scorelabel, (300, 0))

        pygame.display.update()
except:
    pass


if score > highscore:
    with open("highscore.txt", "w") as f:
        f.write(str(score))

while True:
    print("ВЪХ УТРИЕПАХА МАААААААААА")
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background, (0, 0))
    scorelabel = myfont.render("Game Over", 1, (255, 255, 0))
    screen.blit(scorelabel, (150, 150))
    if score > highscore:
        scorelabel = myfont.render("NEW HIGHSCORE - {}!!!".format(score), 1, (255, 255, 0))
        screen.blit(scorelabel, (150, 180))

    pygame.display.update()
