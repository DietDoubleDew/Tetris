
# enumeration support
from enum import Enum

import sys, pygame, random
pygame.init()

print (pygame.font.get_fonts())
sysFont = pygame.font.SysFont(None, 36)

screenSize = (800, 600)

# level and timing
# some information referenced from https://www.colinfahey.com/tetris/tetris.html
currentLevel = 1
cellTransitionTime = ((11 - currentLevel) * 0.05) * 1000 # in milliseconds
lastTransitionTimestamp = 0

allPieces = []
currentPiece = None

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

# grid type
class GridType(Enum):
    Stats = 1
    Board = 2

# a grid piece
class GridPiece():
    def __init__(self, kind):
        self.kind = kind
        if self.kind == Piece.Tee:
            self.height = 2
            self.width = 3
        elif self.kind == Piece.Jay:
            self.height = 2
            self.width = 3
        elif self.kind == Piece.Zee:
            self.height = 2
            self.width = 3
        elif self.kind == Piece.Blk:
            self.height = 2
            self.width = 2
        elif self.kind == Piece.Ess:
            self.height = 2
            self.width = 3
        elif self.kind == Piece.Ell:
            self.height = 2
            self.width = 3
        elif self.kind == Piece.Bar:
            self.height = 1
            self.width = 4

    xpos = int(boardWidthUnits / 2) - 1
    ypos = -1
    rotation = 0
    locked = False
    height = 0
    width = 0

    def drop(self):
        # do a hit test
        if self.ypos == boardHeightUnits - self.height:
            self.locked = True
        
        if self.locked == False:
            self.ypos = self.ypos + 1            

    def draw(self):
        drawPiece(GridType.Board, self.kind, self.xpos, self.ypos)            
        

# initialize the scoreboard
def initScore():
    white = (255, 255, 255)
    scoreLabel = "SCORE"
    scoreValue = "000000"
    imgLabel = sysFont.render(scoreLabel, True, white)
    imgValue = sysFont.render(scoreValue, True, white)
    screen.blit(imgLabel, (600, 100))
    screen.blit(imgValue, (600, 130))

# initialize the stats area
def initStats():
    color = (0, 240, 0)
    for y in range(statsHeightUnits):
        for x in range(statsWidthUnits):
            left = statsLeft + (statsUnitLength * x)
            top = statsTop + (statsUnitLength * y)
            width = statsUnitLength
            height = statsUnitLength
            square = pygame.Rect(left, top, width, height)
            pygame.draw.rect(screen, color, square, 2)

    # put the piece count indicators
    drawPiece(GridType.Stats, Piece.Tee, 2, 3)
    drawPiece(GridType.Stats, Piece.Jay, 2, 6)
    drawPiece(GridType.Stats, Piece.Zee, 2, 9)
    drawPiece(GridType.Stats, Piece.Blk, 2, 12)
    drawPiece(GridType.Stats, Piece.Ess, 2, 15)
    drawPiece(GridType.Stats, Piece.Ell, 2, 18)
    drawPiece(GridType.Stats, Piece.Bar, 2, 21)

    # put the numbers next to it
    statsLabel = "STATISTICS"
    white = (255, 255, 255)
    imgLabel = sysFont.render(statsLabel, True, white)    
    screen.blit(imgLabel, (statsLeft + 5, statsTop + 5))

    drawPieceCount(3, 0)
    drawPieceCount(6, 1)
    drawPieceCount(9, 3)
    drawPieceCount(12, 0)
    drawPieceCount(15, 2)
    drawPieceCount(18, 5)
    drawPieceCount(21, 4)

# draw piece count
def drawPieceCount(ypos, count):
    label = format(count, "03d")
    white = (255, 255, 255)
    image = sysFont.render(label, True, white)
    midway = int((statsUnitLength * statsWidthUnits) / 2)
    height = statsTop + (ypos * statsUnitLength)
    screen.blit(image, (statsLeft + midway + 20, height))

# initialize the board only once
def initBoard():
    color = (240, 0, 0)        
    for y in range(boardHeightUnits):
        for x in range(boardWidthUnits):
            left = boardLeft + (boardUnitLength * x)
            top = boardTop + (boardUnitLength * y)
            width = boardUnitLength
            height = boardUnitLength
            square = pygame.Rect(left, top, width, height)
            pygame.draw.rect(screen, color, square, 2)

# draw piece
def drawPiece(grid, piece, xpos, ypos):
    # all white for now
    color = (255, 255, 255)

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

    rect1 = pygame.Rect(0, 0, 0, 0)
    rect2 = pygame.Rect(0, 0, 0, 0)
    rect3 = pygame.Rect(0, 0, 0, 0)
    rect4 = pygame.Rect(0, 0, 0, 0)

    if piece == Piece.Tee:        
        rect1 = getRectFromPos(left, top, unit, xpos, ypos)
        rect2 = getRectFromPos(left, top, unit, xpos+1, ypos)
        rect3 = getRectFromPos(left, top, unit, xpos+1, ypos+1)
        rect4 = getRectFromPos(left, top, unit, xpos+2, ypos)
        
    elif piece == Piece.Jay:
        rect1 = getRectFromPos(left, top, unit, xpos, ypos)
        rect2 = getRectFromPos(left, top, unit, xpos+1, ypos)
        rect3 = getRectFromPos(left, top, unit, xpos+2, ypos)
        rect4 = getRectFromPos(left, top, unit, xpos+2, ypos+1)

    elif piece == Piece.Zee:
        rect1 = getRectFromPos(left, top, unit, xpos, ypos)
        rect2 = getRectFromPos(left, top, unit, xpos+1, ypos)
        rect3 = getRectFromPos(left, top, unit, xpos+1, ypos+1)
        rect4 = getRectFromPos(left, top, unit, xpos+2, ypos+1)

    elif piece == Piece.Blk:
        rect1 = getRectFromPos(left, top, unit, xpos, ypos)
        rect2 = getRectFromPos(left, top, unit, xpos, ypos+1)
        rect3 = getRectFromPos(left, top, unit, xpos+1, ypos)
        rect4 = getRectFromPos(left, top, unit, xpos+1, ypos+1)

    elif piece == Piece.Ess:
        rect1 = getRectFromPos(left, top, unit, xpos, ypos+1)
        rect2 = getRectFromPos(left, top, unit, xpos+1, ypos+1)
        rect3 = getRectFromPos(left, top, unit, xpos+1, ypos)
        rect4 = getRectFromPos(left, top, unit, xpos+2, ypos)

    elif piece == Piece.Ell:
        rect1 = getRectFromPos(left, top, unit, xpos, ypos)
        rect2 = getRectFromPos(left, top, unit, xpos, ypos+1)
        rect3 = getRectFromPos(left, top, unit, xpos+1, ypos)
        rect4 = getRectFromPos(left, top, unit, xpos+2, ypos)

    elif piece == Piece.Bar:
        rect1 = getRectFromPos(left, top, unit, xpos, ypos)
        rect2 = getRectFromPos(left, top, unit, xpos+1, ypos)
        rect3 = getRectFromPos(left, top, unit, xpos+2, ypos)
        rect4 = getRectFromPos(left, top, unit, xpos+3, ypos)

    # draw the four blocks
    pygame.draw.rect(screen, color, rect1)
    pygame.draw.rect(screen, color, rect2)
    pygame.draw.rect(screen, color, rect3)
    pygame.draw.rect(screen, color, rect4)
        

def getRectFromPos(leftStart, topStart, unitLength, xpos, ypos):
    left = leftStart + (xpos * unitLength)
    top = topStart + (ypos * unitLength)
    return pygame.Rect(left, top, unitLength, unitLength)


# render the pieces
def renderPieces():
    global lastTransitionTimestamp
    global cellTransitionTime
    currentTime = pygame.time.get_ticks()
    if currentTime > (lastTransitionTimestamp + cellTransitionTime):
        print("rendering at " + str(currentTime) + " with transition time " + str(cellTransitionTime))
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
            currentPiece = GridPiece(Piece(nextPiece))
            allPieces.append(currentPiece)
            
        # render all the pieces
        for piece in allPieces:
            piece.drop()
            piece.draw()
            

# main game loop
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # let's display a grid of squares
    if boardInitialized == False:
        initBoard()
        initStats()
        initScore()
        
        boardInitialized = True

    # draw next piece
    renderPieces()

    # display the screen
    pygame.display.flip()

    # wait for one frame
    pygame.time.wait(30)


