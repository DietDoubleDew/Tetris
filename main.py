
# enumeration support
from enum import Enum

import sys, pygame, random
pygame.init()

sysFont = pygame.font.SysFont(None, 36)

screenWidth = 800
screenHeight = 600
screenSize = (screenWidth, screenHeight)

# level and timing
# some information referenced from https://www.colinfahey.com/tetris/tetris.html
currentLevel = 10
cellTransitionTime = ((11 - currentLevel) * 0.05) * 1000 # in milliseconds
lastTransitionTimestamp = 0
g_gameOver = False

# speed to increase to temporarily while forcing down
forceDown = False
forceDownMultiplier = 6.0

allPieces = []
currentPiece = None

# load our image resources
imgBlkTeal = pygame.image.load("graphics\\blk_teal.bmp")
imgBlkGreen = pygame.image.load("graphics\\blk_green.bmp")
imgBlkBlue = pygame.image.load("graphics\\blk_blue.bmp")
imgBlkPurple = pygame.image.load("graphics\\blk_purple.bmp")
imgBlkOrange = pygame.image.load("graphics\\blk_orange.bmp")
imgBlkRed = pygame.image.load("graphics\\blk_red.bmp")
imgBlkYellow = pygame.image.load("graphics\\blk_yellow.bmp")

# inner board specifications
boardWidthUnits = 10
boardHeightUnits = 20
boardUnitLength = 23
boardLeft = 300
boardTop = 65
boardWidthPixels = boardWidthUnits * boardUnitLength
boardHeightPixels = boardHeightUnits * boardUnitLength

# stats section
statsWidthUnits = 10
statsHeightUnits = 25
statsUnitLength = 15
statsLeft = 70
statsTop = 130

imgStatsTeal = pygame.transform.scale(imgBlkTeal, (statsUnitLength, statsUnitLength))
imgStatsGreen = pygame.transform.scale(imgBlkGreen, (statsUnitLength, statsUnitLength))
imgStatsBlue = pygame.transform.scale(imgBlkBlue, (statsUnitLength, statsUnitLength))
imgStatsPurple = pygame.transform.scale(imgBlkPurple, (statsUnitLength, statsUnitLength))
imgStatsOrange = pygame.transform.scale(imgBlkOrange, (statsUnitLength, statsUnitLength))
imgStatsRed = pygame.transform.scale(imgBlkRed, (statsUnitLength, statsUnitLength))
imgStatsYellow = pygame.transform.scale(imgBlkYellow, (statsUnitLength, statsUnitLength))

# set screen mode
screen = pygame.display.set_mode(screenSize)

boardInitialized = False

# piece types
class Piece(Enum):
    Tee = 1
    Jay = 2
    Zee = 3
    Blk = 4
    Ess = 5
    Ell = 6
    Bar = 7

# piece colors
class PieceColor(Enum):
    Teal = 1
    Green = 2
    Blue = 3
    Purple = 4
    Orange = 5
    Red = 6
    Yellow = 7

# grid type
class GridType(Enum):
    Stats = 1
    Board = 2

# statistics board
class StatsSection():
    TeeCount = 0
    JayCount = 0
    ZeeCount = 0
    BlkCount = 0
    EssCount = 0
    EllCount = 0
    BarCount = 0

    # update the count
    def updateCount(self, kind):
        if kind == Piece.Tee:
            self.TeeCount += 1
        elif kind == Piece.Jay:
            self.JayCount += 1
        elif kind == Piece.Zee:
            self.ZeeCount += 1
        elif kind == Piece.Blk:
            self.BlkCount += 1
        elif kind == Piece.Ess:
            self.EssCount += 1
        elif kind == Piece.Ell:
            self.EllCount += 1
        elif kind == Piece.Bar:
            self.BarCount += 1

        # draw it
        self.drawStats()

    # initialize the stats area
    def drawStats(self):

        # clear the whole section
        black = (0,0,0)
        width = statsWidthUnits * statsUnitLength
        height = statsHeightUnits * statsUnitLength
        cover = pygame.Rect(statsLeft, statsTop, width, height)
        pygame.draw.rect(screen, black, cover)
        
        # draw the box border
        color = (255, 255, 255)        
        rect = pygame.Rect(statsLeft, statsTop, width, height)
        pygame.draw.rect(screen, color, rect, 2)

        # put the piece count indicators
        drawPiece(GridType.Stats, GridPiece(Piece.Tee, 2, 3))
        drawPiece(GridType.Stats, GridPiece(Piece.Jay, 2, 6))
        drawPiece(GridType.Stats, GridPiece(Piece.Zee, 2, 9))
        drawPiece(GridType.Stats, GridPiece(Piece.Blk, 2, 12))
        drawPiece(GridType.Stats, GridPiece(Piece.Ess, 2, 15))
        drawPiece(GridType.Stats, GridPiece(Piece.Ell, 2, 18))
        drawPiece(GridType.Stats, GridPiece(Piece.Bar, 2, 21))

        # put the numbers next to it
        statsLabel = "STATISTICS"
        white = (255, 255, 255)
        imgLabel = sysFont.render(statsLabel, True, white)    
        screen.blit(imgLabel, (statsLeft + 5, statsTop + 5))

        drawPieceCount(3, self.TeeCount)
        drawPieceCount(6, self.JayCount)
        drawPieceCount(9, self.ZeeCount)
        drawPieceCount(12, self.BlkCount)
        drawPieceCount(15, self.EssCount)
        drawPieceCount(18, self.EllCount)
        drawPieceCount(21, self.BarCount)


# create the stats section
g_statsSection = StatsSection()

# game over screen
def gameOver():
    global g_gameOver
    color = (244, 244, 244)
    cover = pygame.Rect(screenWidth / 10, screenHeight / 10, (screenWidth / 10) * 8, (screenHeight / 10) * 8)
    pygame.draw.rect(screen, color, cover)
    g_gameOver = True

    textColor = (40, 50, 60)
    message = "Try again some other time bro.  YOU LOST!"
    imgMsg = sysFont.render(message, True, textColor)
    screen.blit(imgMsg, (screenWidth / 9,  screenHeight / 7))
    message = "But don't worry, no one has to know."
    imgMsg = sysFont.render(message, True, textColor)
    screen.blit(imgMsg, (screenWidth / 9, (screenHeight / 7) + 30))

# a grid piece
class GridPiece():
    def __init__(self, kind, xpos, ypos):
        self.kind = kind
        self.xpos = xpos
        self.ypos = ypos
        
        if self.kind == Piece.Tee:
            self.height = 2
            self.width = 3
            self.color = PieceColor.Purple
        elif self.kind == Piece.Jay:
            self.height = 2
            self.width = 3
            self.color = PieceColor.Blue
        elif self.kind == Piece.Zee:
            self.height = 2
            self.width = 3
            self.color = PieceColor.Red
        elif self.kind == Piece.Blk:
            self.height = 2
            self.width = 2
            self.color = PieceColor.Yellow
        elif self.kind == Piece.Ess:
            self.height = 2
            self.width = 3
            self.color = PieceColor.Green
        elif self.kind == Piece.Ell:
            self.height = 2
            self.width = 3
            self.color = PieceColor.Orange
        elif self.kind == Piece.Bar:
            self.height = 1
            self.width = 4
            self.color = PieceColor.Teal
            
    rotation = 0
    locked = False

    def drop(self):
        # do a hit test
        if self.ypos == boardHeightUnits - self.height:
            self.locked = True

        #check against all other blocks
        myPoints = self.positions()
        for blk in allPieces:
            if blk is not self:
                yourPoints = blk.positions()
                for yourPoint in yourPoints:
                    for myPoint in myPoints:
                        if yourPoint[0] == myPoint[0] and yourPoint[1] == myPoint[1] + 1:
                            self.locked = True
                            break
                    if self.locked == True:
                        break
                if self.locked == True:
                    break

        if self.locked == False:
            self.ypos = self.ypos + 1

        # if we are locked and we haven't moved
        # the game is over
        if self.locked == True and self.ypos == -1:
            gameOver()

        return not self.locked

    def draw(self):
        drawPiece(GridType.Board, self)            
        

    def positions(self):
        points = []
        if self.kind == Piece.Tee:
            points.append([self.xpos, self.ypos])
            points.append([self.xpos+1, self.ypos])
            points.append([self.xpos+1, self.ypos+1])
            points.append([self.xpos+2, self.ypos])
        elif self.kind == Piece.Jay:
            points.append([self.xpos, self.ypos])
            points.append([self.xpos+1, self.ypos])
            points.append([self.xpos+2, self.ypos])
            points.append([self.xpos+2, self.ypos+1])
        elif self.kind == Piece.Zee:
            points.append([self.xpos, self.ypos])
            points.append([self.xpos+1, self.ypos])
            points.append([self.xpos+1, self.ypos+1])
            points.append([self.xpos+2, self.ypos+1])
        elif self.kind == Piece.Blk:
            points.append([self.xpos, self.ypos])
            points.append([self.xpos, self.ypos+1])
            points.append([self.xpos+1, self.ypos])
            points.append([self.xpos+1, self.ypos+1])
        elif self.kind == Piece.Ess:
            points.append([self.xpos, self.ypos+1])
            points.append([self.xpos+1, self.ypos+1])
            points.append([self.xpos+1, self.ypos])
            points.append([self.xpos+2, self.ypos])
        elif self.kind == Piece.Ell:
            points.append([self.xpos, self.ypos])
            points.append([self.xpos, self.ypos+1])
            points.append([self.xpos+1, self.ypos])
            points.append([self.xpos+2, self.ypos])
        elif self.kind == Piece.Bar:
            points.append([self.xpos, self.ypos])
            points.append([self.xpos+1, self.ypos])
            points.append([self.xpos+2, self.ypos])
            points.append([self.xpos+3, self.ypos])

        return points

# initialize the scoreboard
def initScore():
    white = (255, 255, 255)
    scoreLabel = "SCORE"
    scoreValue = "000000"
    imgLabel = sysFont.render(scoreLabel, True, white)
    imgValue = sysFont.render(scoreValue, True, white)
    screen.blit(imgLabel, (600, 100))
    screen.blit(imgValue, (600, 130))



# draw piece count
def drawPieceCount(ypos, count):
    label = format(count, "03d")
    white = (255, 255, 255)
    image = sysFont.render(label, True, white)
    midway = int((statsUnitLength * statsWidthUnits) / 2)
    height = statsTop + (ypos * statsUnitLength)
    screen.blit(image, (statsLeft + midway + 20, height))

# convert piece color to bitmap
def pieceColorToImg(grid, color):
    if color == PieceColor.Teal:
        if grid == GridType.Stats:
            return imgStatsTeal
        else:
            return imgBlkTeal
    elif color == PieceColor.Blue:
        if grid == GridType.Stats:
            return imgStatsBlue
        else:
            return imgBlkBlue
    elif color == PieceColor.Green:
        if grid == GridType.Stats:
            return imgStatsGreen
        else:
            return imgBlkGreen
    elif color == PieceColor.Orange:
        if grid == GridType.Stats:
            return imgStatsOrange
        else:
            return imgBlkOrange
    elif color == PieceColor.Purple:
        if grid == GridType.Stats:
            return imgStatsPurple
        else:
            return imgBlkPurple
    elif color == PieceColor.Red:
        if grid == GridType.Stats:
            return imgStatsRed
        else:
            return imgBlkRed
    elif color == PieceColor.Yellow:
        if grid == GridType.Stats:
            return imgStatsYellow
        else:
            return imgBlkYellow

# draw piece using bitmaps
def drawPiece(grid, piece):
    left = 0
    top = 0
    unit = 0

    if grid == GridType.Stats:
        left = statsLeft
        top = statsTop
        unit = statsUnitLength
    elif grid == GridType.Board:
        left = boardLeft
        top = boardTop
        unit = boardUnitLength

    pieceImg = pieceColorToImg(grid, piece.color)

    # get the positions and draw them
    points = piece.positions()
    for point in points:
        screen.blit(pieceImg, (left + (point[0] * unit), top + (point[1] * unit)))

# render the pieces
def renderPieces():
    global lastTransitionTimestamp
    global cellTransitionTime
    global forceDown

    currentTime = pygame.time.get_ticks()
    transitionTime = cellTransitionTime

    # if someone is holding down, we decrease the transition time
    if forceDown == True:
        transitionTime = transitionTime / forceDownMultiplier
    
    if currentTime > (lastTransitionTimestamp + transitionTime):
        print("rendering at " + str(currentTime) + " with transition time " + str(transitionTime))
        lastTransitionTimestamp = currentTime

        # what piece are we working with?
        white = (255, 255, 255)
        black = (0, 0, 0)
        for y in range(boardHeightUnits):
            for x in range(boardWidthUnits):
                left = boardLeft + (boardUnitLength * x)
                top = boardTop + (boardUnitLength * y)
                width = boardUnitLength
                height = boardUnitLength
                square = pygame.Rect(left, top, width, height)
                pygame.draw.rect(screen, black, square)

        # draw one box around the main board
        width = boardUnitLength * boardWidthUnits
        height = boardUnitLength * boardHeightUnits
        square = pygame.Rect(boardLeft, boardTop, width, height)
        pygame.draw.rect(screen, white, square, 2)

        # if we don't have a current piece, create one
        global currentPiece
        if currentPiece == None:
            nextPiece = random.randint(1, 7)
            currentPiece = GridPiece(Piece(nextPiece), int(boardWidthUnits / 2) - 1, -1)
            allPieces.append(currentPiece)
            g_statsSection.updateCount(currentPiece.kind)
            
        # render all the pieces
        dropping = False
        for piece in allPieces:
            dropping = piece.drop() or dropping

            # draw the piece is we are still playing
            if g_gameOver == False:
                piece.draw()

        if dropping == False:
            currentPiece = None
            forceDown = False
            print("pieces have stopped dropping")
            

# move left
def moveLeft():
    if currentPiece is not None:
        if currentPiece.xpos > 0:
            currentPiece.xpos -= 1

# move right
def moveRight():
    if currentPiece is not None:
        if currentPiece.xpos < boardWidthUnits - currentPiece.width:
            currentPiece.xpos += 1

# force piece down
def moveDown():
    global forceDown
    forceDown = True

# rotate clockwise
def rotateClockwise():
    if currentPiece is not None:
        currentPiece.rotate(1)

# main game loop
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft()
            elif event.key == pygame.K_RIGHT:
                moveRight()
            elif event.key == pygame.K_DOWN:
                moveDown()
            elif event.key == pygame.K_UP:
                rotateClockwise()

    # let's display a grid of squares
    if boardInitialized == False:
        g_statsSection.drawStats()
        initScore()        
        boardInitialized = True

    # draw next piece if we are still playing
    if g_gameOver == False:        
        renderPieces()

    # display the screen
    pygame.display.flip()

    # wait for one frame
    pygame.time.wait(30)


