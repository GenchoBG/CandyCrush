import pygame, sys, random, math, time
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
imageDiamondSlunce = "images/slunce.png"
imageDead = "images/dead.png"
imageBomb = "images/bomb.png"
imageBomb1 = "images/bomb2.png"
imageBomb2 = "images/bomb3.png"

pygame.init()

screen = pygame.display.set_mode((500, 500), 0, 32)
background = pygame.image.load(backgroundImageDirectory).convert()
border = pygame.image.load(borderImageDirectory).convert_alpha()
dead = pygame.image.load(imageDead).convert_alpha()
bomb = pygame.image.load(imageBomb).convert_alpha()
bomb1 = pygame.image.load(imageBomb2).convert_alpha()
bomb2 = pygame.image.load(imageBomb1).convert_alpha()
bombImage = bomb
bombImages = [bomb, bomb1, bomb2]

gems = {
    "Mandarina": pygame.image.load(imageDiamondMandarina).convert_alpha(),
    "Sinko": pygame.image.load(imageDiamondSinko).convert_alpha(),
    "More": pygame.image.load(imageDiamondMore).convert_alpha(),
    "Emerald": pygame.image.load(imageDiamondEmerald).convert_alpha(),
    "Ruby": pygame.image.load(imageDiamondRubin).convert_alpha(),
    "Ice": pygame.image.load(imageDiamondIce).convert_alpha(),
    "Slunce": pygame.image.load(imageDiamondSlunce).convert_alpha(),
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

pygame.mixer.music.load("gandalf.mp3")
pygame.mixer.music.play(loops=100)


class Diamond:
    def __init__(self):
        key = random.sample(gems.keys(), 1)[0]
        self.image = gems[key]
        self.type = key
        self.selected = False


class Bomb:
    def __init__(self, range):
        self.type = "bomb"
        self.selected = False
        self.range = range
        if range == 1:
            self.image = bomb
        elif range == 2:
            self.image = bomb1
        else:
            self.image = bomb2


def AfterExplosion():
    toDestroy = []
    for row in grid:
        for diamond in row:
            if diamond.image == dead:
                toDestroy.append(diamond)
    Gravitation(toDestroy)


def Explode(bomb, range):
    global score
    score += 10
    try:
        x, y = GetCoordsFromArray(bomb)
    except:
        return
    grid[x][y].image = dead
    if (range > 0):
        try:
            nextBomb = grid[x + 1][y]
            if nextBomb.image in bombImages:
                Explode(nextBomb, nextBomb.range)
            else:
                Explode(nextBomb, range - 1)
        except:
            pass
        try:
            nextBomb = grid[x - 1][y]
            if nextBomb.image in bombImages:
                Explode(nextBomb, nextBomb.range)
            else:
                Explode(nextBomb, range - 1)
        except:
            pass
        try:
            nextBomb = grid[x][y + 1]
            if nextBomb.image in bombImages:
                Explode(nextBomb, nextBomb.range)
            else:
                Explode(nextBomb, range - 1)
        except:
            pass
        try:
            nextBomb = grid[x][y - 1]
            if nextBomb.image in bombImages:
                Explode(nextBomb, nextBomb.range)
            else:
                Explode(nextBomb, range - 1)
        except:
            pass


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
                grid[row][col].image = dead
        PrintGrid()
        pygame.display.update()
        # time.sleep(0.5)
        for diamond in diamonds:
            if diamond:
                if grid[row][col].type != "dead":
                    grid[row][col].image = gems[grid[row][col].type]

        Gravitation(diamonds)


def Gravitation(diamonds):
    global score
    score += len(diamonds) * 10
    for d in diamonds:
        try:
            x, y = GetCoordsFromArray(d)
        except:
            print(d)
        # print(grid[x][y].type)
        index = y
        while index > 0:
            grid[x][index] = grid[x][index - 1]
            index -= 1
        grid[x][0] = Diamond()
        for i in range(0, 11):
            CheckForDestruction(grid[x][i])


def CheckForDestruction(diamond):
    try:
        diamondX, diamondY = GetCoordsFromArray(diamond)
    except:
        return False
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
        # print(str(len(horizontalDiamonds) + 1) + " horizontalno " + str(horizontalDiamonds[0].type))
        for d in horizontalDiamonds:
            toDestroy.append(d)
    if len(verticalDiamonds) >= 2:
        for d in verticalDiamonds:
            toDestroy.append(d)
            # print(str(len(verticalDiamonds) + 1) + " vertikalno " + str(verticalDiamonds[0].type))
    if len(verticalDiamonds) >= 2 or len(horizontalDiamonds) >= 2:
        if len(verticalDiamonds) >= 3 or len(horizontalDiamonds) >= 3 or (
                        len(verticalDiamonds) >= 2 and len(horizontalDiamonds) >= 2):
            x, y = GetCoordsFromArray(diamond)
            grid[x][y] = Bomb(len(toDestroy) - 2)
        else:
            toDestroy.append(diamond)
        Destroy(toDestroy)

        return True

    return False


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
    try:
        x1, y1 = GetCoordsFromArray(firstDiamond)
        x2, y2 = GetCoordsFromArray(secondDiamond)
        xDifference = abs(x1 - x2)
        yDifference = abs(y1 - y2)
        return (xDifference == 1 and yDifference == 0) or (xDifference == 0 and yDifference == 1)
    except:
        return False


def Swap(firstDiamond, secondDiamond):
    if Adjacent(firstDiamond, secondDiamond):
        x1, y1 = GetCoordsFromArray(firstDiamond)
        x2, y2 = GetCoordsFromArray(secondDiamond)
        temp = grid[x1][y1]
        grid[x1][y1] = grid[x2][y2]
        grid[x2][y2] = temp


def PrintGrid():
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

    scorelabel = myfont.render("Score: " + str(score) + " Time: " + str(60 - seconds), 1, (255, 255, 0))
    screen.blit(scorelabel, (300, 0))


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
                Swap(selectedDiamond, secondDiamond)
                if secondDiamond:
                    selectedDiamond.selected = False
                    if secondDiamond.type == "bomb":
                        Explode(secondDiamond, secondDiamond.range)
                        AfterExplosion()
                    if selectedDiamond.type == "bomb":
                        Explode(selectedDiamond, selectedDiamond.range)
                        AfterExplosion()
                    firstBool = CheckForDestruction(selectedDiamond)
                    secondBool = CheckForDestruction(secondDiamond)
                    if not firstBool and not secondBool:
                        Swap(selectedDiamond, secondDiamond)
                    selectedDiamond = None
                    secondDiamond = None

    if milliseconds > 1000:
        seconds += 1
        milliseconds -= 1000
    '''
    if seconds > 60:
        minutes += 1
        seconds -= 60
    '''

    if seconds == 10:
        break

    milliseconds += clock.tick_busy_loop(60)

    PrintGrid()

    pygame.display.update()

if score > highscore:
    with open("highscore.txt", "w") as f:
        f.write(str(score))

while True:
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